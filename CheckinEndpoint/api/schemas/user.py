from CheckinEndpoint.models import User
from CheckinEndpoint.extensions import ma, db


class UserSchema(ma.SQLAlchemyAutoSchema):

    id = ma.Int(dump_only=True)
    password = ma.String(load_only=True, required=True)
    is_admin = ma.Boolean(dump_only=True)

    class Meta:
        model = User
        sqla_session = db.session
        load_instance = True
