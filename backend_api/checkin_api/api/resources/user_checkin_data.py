from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from checkin_api.api.schemas import UserCheckinDataSchema
from checkin_api.commons.role import admin_required
from checkin_api.models.user import UserCheckinData


class AdminUserCheckinDataResource(Resource):
    """
    管理员查询用户打卡数据的Resource
    """
    method_decorators = [jwt_required, admin_required]

    def get(self, user_id):
        schema = UserCheckinDataSchema()
        data = UserCheckinData.query.get_or_404(user_id)
        return {"checkin_data": schema.dump(data)}, 200


class UserCheckinDataResource(Resource):
    """
    用户打卡数据Resource
    """
    method_decorators = [jwt_required]

    def get(self):
        schema = UserCheckinDataSchema()
        user_id = get_jwt_identity()
        data = UserCheckinData.query.get_or_404(user_id)
        return {"checkin_data": schema.dump(data)}, 200
