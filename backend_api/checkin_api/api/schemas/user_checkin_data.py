from checkin_api.models import UserCheckinData
from checkin_api.extensions import ma, db


class UserCheckinDataSchema(ma.SQLAlchemyAutoSchema):
    """
    用户打卡数据导出模型
    """
    id = ma.Int(dump_only=True)
    username = ma.String(required=True)
    last_checkin_time = ma.DateTime(load_only=False, required=True)
    total_checkin_count = ma.Integer(load_only=False, required=True)
    total_fail_count = ma.Integer(load_only=False, required=True)

    class Meta:
        model = UserCheckinData
        sqla_session = db.session
        load_instance = True
