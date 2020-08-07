from checkin_api.models import User
from checkin_api.extensions import ma, db


class UserSchema(ma.SQLAlchemyAutoSchema):
    """
    用户的数据导出模型
    """
    id = ma.Int(dump_only=True)
    username = ma.String(required=True)
    email = ma.String(required=True)
    password = ma.String(load_only=True, required=True)
    is_admin = ma.Boolean(dump_only=True)

    class Meta:
        model = User
        sqla_session = db.session
        load_instance = True
