from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from checkin_api.api.schemas import UserSchema
from checkin_api.models import User, UserCheckinData
from checkin_api.extensions import db
from checkin_api.commons.pagination import paginate
from checkin_api.commons.role import admin_required
from checkin_api.tasks.user_manage import clean_users


class UserResource(Resource):
    """
    用户自身信息管理Resource
    """
    method_decorators = [jwt_required]

    def get(self):
        user_id = get_jwt_identity()
        schema = UserSchema()
        user = User.query.get(user_id)
        return {"user": schema.dump(user)}

    def put(self):
        user_id = get_jwt_identity()
        schema = UserSchema(partial=True)
        user = User.query.get_or_404(user_id)
        user = schema.load(request.json, instance=user)

        db.session.commit()

        return {"msg": "user updated", "user": schema.dump(user)}


class AdminUserResource(Resource):
    """
    管理员管理用户信息Resource
    """

    method_decorators = [jwt_required, admin_required]

    def get(self, user_id):
        schema = UserSchema()
        user = User.query.get_or_404(user_id)
        return {"user": schema.dump(user)}

    def put(self, user_id):
        schema = UserSchema(partial=True)
        user = User.query.get_or_404(user_id)
        old_name = user.username
        user = schema.load(request.json, instance=user)
        if user.username != old_name:
            user.username = old_name
        db.session.commit()

        return {"msg": "user updated", "user": schema.dump(user)}

    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        # checkin_data = UserCheckinData.query.get_or_404(user_id)
        db.session.delete(user)
        # db.session.delete(checkin_data)
        db.session.commit()

        return {"msg": "user deleted"}


class AdminUserList(Resource):
    """
    用户列表Resource
    """

    method_decorators = [jwt_required, admin_required]

    def get(self):
        schema = UserSchema(many=True)
        query = User.query
        return paginate(query, schema)


class CreateUserResource(Resource):
    """
    注册用户Resource
    """

    def post(self):
        schema = UserSchema()
        user = schema.load(request.json)
        user.is_admin = False

        # 检查是否有用户名重名
        tmp = User.query.filter_by(username=user.username).first()
        if tmp:
            return {'msg': 'username was taken'}, 403

        db.session.add(user)
        db.session.flush()
        # data_schema = UserCheckinDataSchema()
        # checkin_data = data_schema.load(
        #     {"username": user.username, "last_checkin_time": '1990/01/01 08:00:00',
        #      "total_checkin_count": 0, "total_fail_count": 0})
        now = datetime.now()
        now = datetime(now.year, now.month, now.day, 8, 0, 0)
        checkin_data = UserCheckinData(user=user)
        checkin_data.username = user.username
        checkin_data.last_checkin_time = now
        checkin_data.total_checkin_count = 0
        checkin_data.total_fail_count = 0

        db.session.add(checkin_data)
        db.session.commit()

        return {'msg': 'user created', "user": schema.dump(user)}, 200


class UserRecoveryResource(Resource):
    """
    用户找回密码Resource
    """

    def post(self):
        data = request.get_json()

        if any(s in data.keys() for s in ('username', 'email', 'newpassword')):
            user = User.query.filter_by(username=data['username']).first()
            if user and user.email == data['email']:
                user.password = data['newpassword']
                db.session.commit()
                return {'msg': 'User updated'}, 200
            else:
                return {'msg': "User not found or email didn't match"}, 404
        else:
            return {'msg': "Bad inputs"}, 500


class AdminCleanUserResource(Resource):
    """
    管理员清理不活动用户资源
    """

    method_decorators = [jwt_required, admin_required]

    def delete(self):
        clean_users.delay()
        return {'msg': "OK"}, 200
