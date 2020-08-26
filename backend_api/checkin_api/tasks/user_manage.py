from datetime import datetime
from checkin_api.models import User, UserCheckinData
from checkin_api.extensions import celery, db
from checkin_api.tasks.mail import send_removed_mail


@celery.task
def clean_users():
    """
    清理3天以上未成功打卡的用户
    """
    now = datetime.now()
    for data in UserCheckinData.query:
        if (now - data.last_checkin_time).total_seconds() / 3600 / 24 > 2:
            # 3天打卡均未成功，那么删除
            user = User.query.filter_by(username=data.username).first()
            if user.is_admin:
                # 如果是管理员那跳过不删除
                continue
            send_removed_mail(user.username, user.email)
            db.session.delete(user)
            db.session.commit()
    return "OK"
