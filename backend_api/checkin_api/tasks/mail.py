import re
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.header import Header
from email.utils import parseaddr, formataddr
from checkin_api import config
from checkin_api.extensions import celery


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def send_mail(username: str, usermail: str, subject: str, content: str):
    """

    """
    sender = 'api@edlinus.cn'
    # 验证邮箱是否是正确的
    if not re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", usermail):
        return "邮箱格式不合法"
        # 收件人
    receivers = [usermail]

    # 构造邮件数据
    message = MIMEText(content, 'plain', 'utf-8')
    message['From'] = _format_addr('可每打卡平台 <api@edlinus.cn>')
    message['To'] = _format_addr('%s <%s>' % (username, usermail))

    message['Subject'] = Header(subject, 'utf-8').encode()

    try:
        smtpObj = smtplib.SMTP_SSL(config.MAIL_SMTP_HOST, config.MAIL_SMTP_PORT)
        smtpObj.login(config.MAIL_SMTP_USER, config.MAIL_SMTP_PASS)
        smtpObj.sendmail(sender, receivers, message.as_string())
        return "OK"
    except smtplib.SMTPException:
        return "FAILED"


@celery.task
def send_success_mail(username, usermail):
    """
    发送打卡成功邮件任务
    :param username:
    :param usermail
    :return:
    """
    # 构造邮件数据
    content = '【%s】已于【%s】打卡成功' % (username, datetime.now().strftime("%Y-%m-%d %H:%M"))
    subject = '【%s】打卡成功提醒' % datetime.now().strftime("%Y-%m-%d")
    # 发送邮件
    return send_mail(username, usermail, subject, content)


@celery.task
def send_fail_mail(username, usermail):
    """
    发送打卡失败邮件任务
    """
    # 构造邮件数据
    content = '在【%s】尝试给【%s】打卡发生错误，建议手动进行打卡。若您忘记了密码，可登陆小程序重置。若您不再需要打卡服务，可发邮件至admin@edlinus.cn申请销号或等待2日后自动销号。' % (username, datetime.now().strftime("%Y-%m-%d %H:%M"))
    subject = '【%s】！！打卡失败！！提醒' % datetime.now().strftime("%Y-%m-%d")
    # 发送邮件
    return send_mail(username, usermail, subject, content)


@celery.task
def send_removed_mail(username, usermail):
    """
    发送用户被清理邮件
    """
    # 构造邮件数据
    content = '【%s】您好，由于您的账号自动打卡多次失败，为节约公益服务资源，已将该账号移除，如有需要请重新注册，因此带来的不便，请见谅' % username
    subject = '账号移除提醒'
    # 发送邮件
    return send_mail(username, usermail, subject, content)
