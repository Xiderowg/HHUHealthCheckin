from flask import Flask
from flask_cors import CORS
from celery.schedules import crontab
from checkin_api import auth, api
from checkin_api.extensions import db, jwt, migrate, apispec, celery


def create_app(testing=False, cli=False):
    """Application factory, used to create application
    """
    app = Flask("checkin_api")
    app.config.from_object("checkin_api.config")
    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    if testing is True:
        app.config["TESTING"] = True

    configure_extensions(app, cli)
    configure_apispec(app)
    register_blueprints(app)
    init_celery(app)

    return app


def configure_extensions(app, cli):
    """configure flask extensions
    """
    db.init_app(app)
    jwt.init_app(app)

    if cli is True:
        migrate.init_app(app, db)


def configure_apispec(app):
    """Configure APISpec for swagger support
    """
    apispec.init_app(app, security=[{"jwt": []}])
    apispec.spec.components.security_scheme(
        "jwt", {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    )
    apispec.spec.components.schema(
        "PaginatedResult",
        {
            "properties": {
                "total": {"type": "integer"},
                "pages": {"type": "integer"},
                "next": {"type": "string"},
                "prev": {"type": "string"},
            }
        },
    )


def register_blueprints(app):
    """register all blueprints for application
    """
    app.register_blueprint(auth.views.blueprint)
    app.register_blueprint(api.views.blueprint)


def init_celery(app=None):
    app = app or create_app()
    celery.conf.broker_url = app.config["CELERY_BROKER_URL"]
    celery.conf.result_backend = app.config["CELERY_RESULT_BACKEND"]
    celery.conf.update(app.config)

    # 自动签到打卡
    celery.conf.imports = celery.conf.imports + ("checkin_api.tasks.checkin",)
    celery.conf.update(
        timezone='Asia/Shanghai',
        enable_utc=True,
        beat_schedule={
            "auto_checkin": {
                "task": "checkin_api.tasks.checkin.auto_checkin",
                "schedule": crontab(minute=10, hour="*/1"),
                "args": ()
            },
        }
    )

    class ContextTask(celery.Task):
        """Make celery tasks work with Flask app context"""

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
