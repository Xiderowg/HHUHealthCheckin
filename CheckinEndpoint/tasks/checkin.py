import re
import json
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from CheckinEndpoint.extensions import celery
from CheckinEndpoint.models import User
from CheckinEndpoint.api.schemas import UserCheckinDataSchema


@celery.task
def checkin(user: User):
    checkin_schema = UserCheckinDataSchema.query.get(user.id)
    ua = {
        "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"}
    # 登录
    s = requests.session()
    s.get("http://ids.hhu.edu.cn/amserver/UI/Login?goto=http://form.hhu.edu.cn/pdc/form/list", headers=ua)
    pay_load = {"IDToken0": "", "IDToken1": user.username, "IDToken2": user.src_password, "IDButton": "Submit",
                "goto": "aHR0cDovL2Zvcm0uaGh1LmVkdS5jbi9wZGMvZm9ybS9saXN0", "encoded": "true",
                "inputCode": "", "gx_charset": "UTF-8"}
    res = s.post("http://ids.hhu.edu.cn/amserver/UI/Login", data=pay_load, headers=ua)
    # 检查登录结果
    cookies = res.cookies.get_dict()
    if "iPlanetDirectoryPro" not in cookies.keys():
        return "Checkin failed because of wrong username or password"
    # 获取wid和uid
    res = s.get("http://form.hhu.edu.cn/pdc/formDesignApi/S/xznuPIjG", headers=ua)
    soup = BeautifulSoup(res.content, "lxml")
    all_scripts = soup.find_all('script')
    full_script = ""
    for script in all_scripts:
        if len(script.text) > 0:
            full_script = script.text
    scripts = full_script.split('\n')
    try:
        wid_line, uid_line = scripts[7], script[10]
        data_pattern = re.compile(r"['](.*?)[']", re.S)
        wid = re.findall(data_pattern, wid_line)[0]
        uid = re.findall(data_pattern, uid_line)[0]
    except IndexError:
        return "Checkin failed on getting wid and uid"
    # 计算最终的API入口
    api_url = "http://form.hhu.edu.cn/pdc/formDesignApi/dataFormSave?wid=%s&userId=%s" % (wid, uid)
    # 读取历史填报信息
    fill_data_line = scripts[119][12:-1:1]
    fill_data = json.loads(fill_data_line)[0]
    del fill_data["CLRQ"]
    del fill_data["USERID"]
    checkin_data = fill_data
    checkin_data["DATETIME_CYCLE"] = datetime.now().strftime("%Y/%m/%d")
    # 打卡
    res = s.post(api_url, checkin_data)
    if res.status_code == 200:
        return "OK"
    else:
        return "Checkin failed on last procedure"
