from CheckinEndpoint.models import UserCheckinData
from CheckinEndpoint.extensions import ma, db


class UserCheckinDataSchema(ma.SQLAlchemyAutoSchema):
    id = ma.Int(dump_only=True)
    username = ma.String(load_only=True, required=True)
    last_checkin_time = ma.DateTime(load_only=False, required=True)
    total_checkin_count = ma.Integer(load_only=False, required=True)
    total_fail_count = ma.Integer(load_only=False, required=True)

    class Meta:
        model = UserCheckinData
        sqla_session = db.session
        load_instance = True
