from flask_restful import Resource
from flask_jwt_extended import jwt_required

from CheckinEndpoint.api.schemas import UserCheckinDataSchema
from CheckinEndpoint.models.user import UserCheckinData


class UserCheckinDataResource(Resource):
    """
    用户打卡数据Resource
    """
    method_decorators = [jwt_required]

    def get(self, user_id):
        schema = UserCheckinDataSchema()
        data = UserCheckinData.query.get_or_404(user_id)
        return {"checkin_data": schema.dump(data)}
