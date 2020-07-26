FLASK_ENV=development
FLASK_APP=CheckinEndpoint.app:create_app
SECRET_KEY=hhuniubi
DATABASE_URI=sqlite:////tmp/CheckinEndpoint.db
CELERY_BROKER_URL=amqp://guest:guest@localhost/
CELERY_RESULT_BACKEND_URL=amqp://guest:guest@localhost/
