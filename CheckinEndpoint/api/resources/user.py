from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from CheckinEndpoint.api.schemas import UserSchema, UserCheckinDataSchema
from CheckinEndpoint.models import User, UserCheckinData
from CheckinEndpoint.extensions import db
from CheckinEndpoint.commons.pagination import paginate
from CheckinEndpoint.commons.role import admin_required


class UserResource(Resource):
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
    """Single object resource

    ---
    get:
      tags:
        - api
      parameters:
        - in: path
          name: user_id
          schema:
            type: integer
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  user: UserSchema
        404:
          description: user does not exists
    put:
      tags:
        - api
      parameters:
        - in: path
          name: user_id
          schema:
            type: integer
      requestBody:
        content:
          application/json:
            schema:
              UserSchema
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: user updated
                  user: UserSchema
        404:
          description: user does not exists
    delete:
      tags:
        - api
      parameters:
        - in: path
          name: user_id
          schema:
            type: integer
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: user deleted
        404:
          description: user does not exists
    """

    method_decorators = [jwt_required, admin_required]

    def get(self, user_id):
        schema = UserSchema()
        user = User.query.get(user_id)
        return {"user": schema.dump(user)}

    def put(self, user_id):
        schema = UserSchema(partial=True)
        user = User.query.get_or_404(user_id)
        user = schema.load(request.json, instance=user)

        db.session.commit()

        return {"msg": "user updated", "user": schema.dump(user)}

    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        checkin_data = UserCheckinData.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.delete(checkin_data)
        db.session.commit()

        return {"msg": "user deleted"}


class AdminUserList(Resource):
    """Creation and get_all

    ---
    get:
      tags:
        - api
      responses:
        200:
          content:
            application/json:
              schema:
                allOf:
                  - $ref: '#/components/schemas/PaginatedResult'
                  - type: object
                    properties:
                      results:
                        type: array
                        items:
                          $ref: '#/components/schemas/UserSchema'
    post:
      tags:
        - api
      requestBody:
        content:
          application/json:
            schema:
              UserSchema
      responses:
        201:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: user created
                  user: UserSchema
    """

    method_decorators = [jwt_required, admin_required]

    def get(self):
        schema = UserSchema(many=True)
        query = User.query
        return paginate(query, schema)


class CreateUserResource(Resource):
    """
    注册用户
    """

    def post(self):
        schema = UserSchema()
        user = schema.load(request.json)
        user.is_admin = False

        data_schema = UserCheckinDataSchema()
        checkin_data = data_schema.load(
            {"id": user.id, "username": user.username, "last_checkin_time": datetime(1990, 1, 1),
             "total_checkin_count": 0, "total_fail_count": 0})

        db.session.add(user)
        db.session.add(checkin_data)
        db.session.commit()

        return {"msg": "user created", "user": schema.dump(user)}, 201
