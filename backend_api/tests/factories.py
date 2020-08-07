import factory
from datetime import datetime
from checkin_api.models import User, UserCheckinData


class UserFactory(factory.Factory):
    username = factory.Sequence(lambda n: "user%d" % n)
    email = factory.Sequence(lambda n: "user%d@mail.com" % n)
    password = "mypwd"

    class Meta:
        model = User


class UserCheckinDataFactory(factory.Factory):
    username = factory.Sequence(lambda n: "user%d" % n)
    last_checkin_time = datetime.now()
    total_checkin_count = 0
    total_fail_count = 0

    class Meta:
        model = UserCheckinData
