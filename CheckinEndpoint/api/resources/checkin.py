from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from CheckinEndpoint.models import User
from CheckinEndpoint.tasks.checkin import checkin
from CheckinEndpoint.commons.role import admin_required


class CheckinResource(Resource):
    method_decorators = [jwt_required]

    def post(self):
        """
        用户给自个儿打卡
        :return:
        """
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user:
            checkin.delay(user)
            return {"msg", "task started"}, 201
        else:
            return {"msg", "wrong user id"}, 400


class AdminCheckinResource(Resource):
    method_decorators = [jwt_required, admin_required]

    def post(self):
        """
        给所有用户打卡
        :return:
        """
        query = User.query
        for user in query:
            checkin.delay(user)
        return {"msg", "tasks started"}, 201
