"""
程序扩展
说明： Singleton成全局变量
"""
from flask_sqlalchemy import SQLAlchemy
from passlib.context import CryptContext
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_cors import CORS
from celery import Celery

from checkin_api.commons.apispec import APISpecExt

db = SQLAlchemy()
jwt = JWTManager()
cors = CORS()
ma = Marshmallow()
migrate = Migrate()
apispec = APISpecExt()
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
celery = Celery()
