from checkin_api.app import init_celery

app = init_celery()
app.conf.imports = app.conf.imports + ("checkin_api.tasks.checkin", "checkin_api.tasks.mail", "checkin_api.tasks.user_manage",)
