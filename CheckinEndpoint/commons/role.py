from functools import wraps

from flask import jsonify
from flask_jwt_extended import (
    verify_jwt_in_request, get_jwt_claims
)


def admin_required(fn):
    """
    管理员wrapper
    :param fn:
    :return:
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if not claims["is_admin"]:
            return jsonify(msg='This API can only be accessed by Admin!'), 403
        else:
            return fn(*args, **kwargs)

    return wrapper
