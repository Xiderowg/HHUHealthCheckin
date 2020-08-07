"""
配置文件
说明：大部分都从环境变量里面读了，方便容器化
"""
import os
from dotenv import load_dotenv
import sys

gettrace = getattr(sys, 'gettrace', None)
if gettrace is None:
    load_dotenv(".flaskenv")
else:
    load_dotenv(".testenv")

ENV = os.getenv("FLASK_ENV")
DEBUG = ENV == "development"
SECRET_KEY = os.getenv("SECRET_KEY")

SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
SQLALCHEMY_TRACK_MODIFICATIONS = False

JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND_URL")

MAIL_SMTP_HOST = os.getenv("MAIL_SMTP_HOST")
MAIL_SMTP_PORT = os.getenv("MAIL_SMTP_PORT")
MAIL_SMTP_USER = os.getenv("MAIL_SMTP_USER")
MAIL_SMTP_PASS = os.getenv("MAIL_SMTP_PASS")
