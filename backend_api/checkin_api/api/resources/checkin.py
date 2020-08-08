from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from checkin_api.models import User
from checkin_api.tasks.checkin import checkin
from checkin_api.commons.role import admin_required


class CheckinResource(Resource):
    """
    普通用户打卡Resource
    """
    method_decorators = [jwt_required]

    def post(self):
        """
        用户给自个儿打卡
        :return:
        """
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        if user is not None:
            checkin.delay(user.username, user.password, user.email, user.is_admin)
            return {'msg': 'task started'}, 200
        else:
            return {'msg': 'wrong user id'}, 400


class AdminCheckinResource(Resource):
    """
    管理员用户打卡Resource
    """
    method_decorators = [jwt_required, admin_required]

    def post(self):
        """
        给所有用户打卡
        :return:
        """
        query = User.query
        for user in query:
            print("now checkin for "+user.username)
            checkin.delay(user.username, user.password, user.email, user.is_admin)
            # print("result:"+ret)
        return {'msg': 'tasks started'}, 200
