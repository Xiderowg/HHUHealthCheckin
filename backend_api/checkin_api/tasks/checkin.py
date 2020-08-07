import re
import json
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import parseaddr, formataddr
from checkin_api import config
from checkin_api.extensions import celery, db
from checkin_api.models import User, UserCheckinData


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


@celery.task
def sendmail(username, usermail):
    """
    发送邮件任务
    :param username:
    :param usermail
    :return:
    """
    sender = 'api@edlinus.cn'
    # 验证邮箱是否是正确的
    if not re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", usermail):
        return "邮箱格式不合法"

    # 收件人
    receivers = [usermail]

    # 构造邮件数据
    content = '【%s】已于【%s】打卡成功' % (username, datetime.now().strftime("%Y-%m-%d %H:%M"))
    message = MIMEText(content, 'plain', 'utf-8')
    message['From'] = _format_addr('可彡每彳亍打卡平台 <api@edlinus.cn>')
    message['To'] = _format_addr('%s <%s>' % (username, usermail))

    subject = '【%s】打卡成功提醒' % datetime.now().strftime("%Y-%m-%d %H:%M")
    message['Subject'] = Header(subject, 'utf-8').encode()

    try:
        smtpObj = smtplib.SMTP_SSL(config.MAIL_SMTP_HOST, config.MAIL_SMTP_PORT)
        smtpObj.login(config.MAIL_SMTP_USER, config.MAIL_SMTP_PASS)
        smtpObj.sendmail(sender, receivers, message.as_string())
        return "OK"
    except smtplib.SMTPException:
        return "FAILED"


@celery.task
def checkin(username, password, email, is_admin):
    """
    打卡任务
    """
    # 如果是管理员，那就不打卡
    if is_admin:
        return "OK"
    # 查找用户打卡记录
    user_checkin_data = UserCheckinData.query.filter_by(username=username).first()
    if user_checkin_data is None:
        return "User's checkin data not found"
    # 如果今天晚6点以后打卡过了，就不打了
    if user_checkin_data.last_checkin_time.hour >= 18 and user_checkin_data.last_checkin_time.day == datetime.now().day:
        return "OK"
    # 开始打卡
    ua = {
        "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"}
    # 登录
    s = requests.session()
    s.get("http://ids.hhu.edu.cn/amserver/UI/Login?goto=http://form.hhu.edu.cn/pdc/form/list", headers=ua)
    pay_load = {"IDToken0": "", "IDToken1": username, "IDToken2": password, "IDButton": "Submit",
                "goto": "aHR0cDovL2Zvcm0uaGh1LmVkdS5jbi9wZGMvZm9ybS9saXN0", "encoded": "true",
                "inputCode": "", "gx_charset": "UTF-8"}
    res = s.post("http://ids.hhu.edu.cn/amserver/UI/Login", data=pay_load, headers=ua)
    # 检查登录结果
    cookies = s.cookies.get_dict()
    if "iPlanetDirectoryPro" not in cookies.keys():
        return "Checkin failed because of wrong username or password"
    # 获取wid和uid
    res = s.get("http://form.hhu.edu.cn/pdc/formDesignApi/S/xznuPIjG", headers=ua)
    soup = BeautifulSoup(res.content, "lxml")
    all_scripts = soup.find_all('script')
    full_script = ""
    for script in all_scripts:
        if '表格集合' in script.text[:18]:
            full_script = script.text
    scripts = full_script.split('\n')
    try:
        wid_line, uid_line = scripts[7], scripts[10]
        data_pattern = re.compile(r"['](.*?)[']", re.S)
        wid = re.findall(data_pattern, wid_line)[0]
        uid = re.findall(data_pattern, uid_line)[0]
    except IndexError:
        return "Checkin failed on getting wid and uid"
    # 计算最终的API入口
    api_url = "http://form.hhu.edu.cn/pdc/formDesignApi/dataFormSave?wid=%s&userId=%s" % (wid, uid)
    # 读取历史填报信息
    fill_data_line = scripts[120][25:-1:1]
    fill_data = json.loads(fill_data_line)[0]
    del fill_data["CLRQ"]
    del fill_data["USERID"]
    checkin_data = fill_data
    checkin_data["DATETIME_CYCLE"] = datetime.now().strftime("%Y/%m/%d")
    # 打卡
    res = s.post(api_url, checkin_data)
    if res.status_code == 200:
        user_checkin_data.last_checkin_time = datetime.now()
        user_checkin_data.total_checkin_count += 1
        db.session.commit()
        sendmail(username, email)
        return "OK"
    else:
        user_checkin_data.total_fail_count += 1
        db.session.commit()
        return "Checkin failed on last procedure"


@celery.task
def auto_checkin():
    """
    自动打卡任务
    :return:
    """
    for user in User.query:
        checkin(user.username, user.password, user.email, user.is_admin)
