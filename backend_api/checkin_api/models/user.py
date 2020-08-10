from sqlalchemy.orm import relationship

from checkin_api.extensions import db, pwd_context


class UserIdentity(object):
    """
    用户认证信息
    """

    def __init__(self, id: int, is_admin: bool):
        self.id = id
        self.is_admin = is_admin


class UserCheckinData(db.Model):
    """
    用户打卡数据模型
    """
    id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    last_checkin_time = db.Column(db.DateTime, nullable=True)
    total_checkin_count = db.Column(db.Integer)
    total_fail_count = db.Column(db.Integer)

    user = relationship('User', backref='usercheckindatas')

    def __init__(self, **kwargs):
        super(UserCheckinData, self).__init__(**kwargs)


class User(db.Model):
    """
    用户模型
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        # self.src_password = self.password
        # self.password = pwd_context.hash(self.password)

    def __repr__(self):
        return "<User %s>" % self.username
