from CheckinEndpoint.extensions import celery
from CheckinEndpoint.models import UserCheckinData, User
from CheckinEndpoint.api.schemas import UserCheckinDataSchema


@celery.task
def checkin(user: User):
    checkin_schema = UserCheckinDataSchema.query.get(user.id)
    # TODO: 打卡逻辑
    return "OK"
