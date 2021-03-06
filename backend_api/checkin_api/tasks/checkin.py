import re
import json
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from checkin_api.extensions import celery, db
from checkin_api.models import User, UserCheckinData
from checkin_api.tasks.mail import send_fail_mail, send_success_mail


@celery.task
def checkin(username, password, email, is_admin, is_bachelor=False):
    """
    打卡任务
    """
    # 如果是管理员，那就不打卡
    if is_admin:
        return "Admin User OK"
    # 查找用户打卡记录
    user_checkin_data = UserCheckinData.query.filter_by(username=username).first()
    if user_checkin_data is None:
        return "User's checkin data not found"
    # 如果今天晚6点以后打卡过了，就不打了
    if user_checkin_data.last_checkin_time.hour >= 18 and user_checkin_data.last_checkin_time.day == datetime.now().day:
        return "Already Checked OK"
    # 重置今日打卡失败次数
    if user_checkin_data.last_attempt_time.day != datetime.now().day:
        user_checkin_data.today_fail_count = 0
    # 如果今日打卡失败次数超过3，那今日不再打卡
    if user_checkin_data.today_fail_count >= 3:
        return "Failed too many times today, abort"
    # 开始打卡
    ua = {
        "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"}
    # 登录
    s = requests.session()
    try:
        s.get("http://ids.hhu.edu.cn/amserver/UI/Login?goto=http://form.hhu.edu.cn/pdc/form/list", headers=ua,
              timeout=10)
    except requests.exceptions.RequestException:
        # send_fail_mail(username, email)
        return "Timeout on getting initial cookie"
    pay_load = {"IDToken0": "", "IDToken1": username, "IDToken2": password, "IDButton": "Submit",
                "goto": "aHR0cDovL2Zvcm0uaGh1LmVkdS5jbi9wZGMvZm9ybS9saXN0", "encoded": "true",
                "inputCode": "", "gx_charset": "UTF-8"}
    res = s.post("http://ids.hhu.edu.cn/amserver/UI/Login", data=pay_load, headers=ua)
    # 检查登录结果
    cookies = s.cookies.get_dict()
    if "iPlanetDirectoryPro" not in cookies.keys():
        send_fail_mail(username, email)
        user_checkin_data.total_fail_count += 1
        user_checkin_data.today_fail_count += 1
        user_checkin_data.last_attempt_time = datetime.now()
        db.session.commit()
        return "Checkin failed because of wrong username or password"
    # 获取wid和uid
    if is_bachelor:
        res = s.get("http://form.hhu.edu.cn/pdc/formDesignApi/S/gUTwwojq", headers=ua)
    else:
        res = s.get("http://form.hhu.edu.cn/pdc/formDesignApi/S/xznuPIjG", headers=ua)
    soup = BeautifulSoup(res.content, "lxml")
    all_scripts = soup.find_all('script')
    full_script = ""
    for script in all_scripts:
        tmp_script = script.string
        if tmp_script is None or len(tmp_script) < 18:
            continue
        if '表格集合' in tmp_script[:18]:
            full_script = tmp_script
            break
    scripts = full_script.split('\n')
    try:
        wid_line, uid_line = scripts[7], scripts[10]
        data_pattern = re.compile(r"['](.*?)[']", re.S)
        wid = re.findall(data_pattern, wid_line)[0]
        uid = re.findall(data_pattern, uid_line)[0]
    except IndexError:
        user_checkin_data.total_fail_count += 1
        user_checkin_data.today_fail_count += 1
        user_checkin_data.last_attempt_time = datetime.now()
        db.session.commit()
        send_fail_mail(username, email)
        return "Checkin failed on getting wid and uid, detailed script:\n" + full_script
    # 计算最终的API入口
    api_url = "http://form.hhu.edu.cn/pdc/formDesignApi/dataFormSave?wid=%s&userId=%s" % (wid, uid)
    # 读取历史填报信息
    try:
        fill_data_line = scripts[120][25:-1:1]
        fill_data = json.loads(fill_data_line)[0]
        del fill_data["CLRQ"]
        del fill_data["USERID"]
    except IndexError:
        user_checkin_data.total_fail_count += 1
        user_checkin_data.today_fail_count += 1
        user_checkin_data.last_attempt_time = datetime.now()
        db.session.commit()
        send_fail_mail(username, email)
        return "Checkin failed on getting historical data, detailed script:\n" + full_script
    checkin_data = fill_data
    checkin_data["DATETIME_CYCLE"] = datetime.now().strftime("%Y/%m/%d")
    # 打卡
    try:
        res = s.post(api_url, checkin_data, timeout=10)
    except requests.exceptions.RequestException:
        user_checkin_data.total_fail_count += 1
        user_checkin_data.today_fail_count += 1
        user_checkin_data.last_attempt_time = datetime.now()
        db.session.commit()
        send_fail_mail(username, email)
        return "Checkin failed on posting message to server"
    if res.status_code == 200:
        user_checkin_data.last_checkin_time = datetime.now()
        user_checkin_data.last_attempt_time = user_checkin_data.last_checkin_time
        user_checkin_data.total_checkin_count += 1
        user_checkin_data.today_fail_count = 0
        db.session.commit()
        send_success_mail(username, email)
        return "OK"
    else:
        user_checkin_data.total_fail_count += 1
        user_checkin_data.today_fail_count += 1
        user_checkin_data.last_attempt_time = datetime.now()
        db.session.commit()
        send_fail_mail(username, email)
        return "Checkin failed on last procedure"


@celery.task
def auto_checkin():
    """
    自动打卡任务
    :return:
    """
    if datetime.now().minute > 0:
        print("start auto checkin")
        for user in User.query:
            checkin(user.username, user.password, user.email, user.is_admin, user.is_bachelor)
