import click
from flask.cli import FlaskGroup

from checkin_api.app import create_app


def create_checkin_api(info):
    return create_app(cli=True)


@click.group(cls=FlaskGroup, create_app=create_checkin_api)
def cli():
    """
    CLI入口点
    """


@cli.command("init")
def init():
    """
    新建一个管理员角色
    """
    from checkin_api.extensions import db
    from checkin_api.models import User, UserCheckinData
    from datetime import datetime

    click.echo("create user")
    user = User(username="admin", email="admin@edlinus.cn", password="alexlyn", is_admin=True)
    checkin_data = UserCheckinData(id=user.id, username=user.username, last_checkin_time=datetime(1990, 1, 1),
                                   total_checkin_count=0, total_fail_count=0)
    db.session.add(user)
    db.session.add(checkin_data)
    db.session.commit()
    click.echo("created user admin")


if __name__ == "__main__":
    cli()
