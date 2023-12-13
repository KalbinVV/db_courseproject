from functools import wraps
from typing import Callable

import flask
import jwt
from flask import Response, make_response

import models


def has_token(request: flask.request) -> bool:
    return 'token' in request.cookies


def is_user_authed(request: flask.request):
    if not has_token(request):
        return False

    try:
        decode_token(request)

        return True
    except (Exception, ):
        return False


def create_token(user: models.User) -> str:
    encoded_jwt = jwt.encode({"user_id": user.id}, "secret", algorithm="HS256")

    return encoded_jwt


def decode_token(request: flask.request) -> int:
    jwt_token = request.cookies.get('token')

    decoded_jwt = jwt.decode(jwt_token, "secret", algorithms=["HS256"])

    return int(decoded_jwt['user_id'])


def get_user(request: flask.request) -> models.User:
    return models.User.query.filter_by(id=decode_token(request)).first_or_404()


def should_be_authed(function: Callable) -> Callable:
    @wraps(function)
    def decorator(*args, **kwargs) -> Response | str:
        if not is_user_authed(flask.request):
            return make_response("You are not authed", 400)

        return function(*args, **kwargs)

    return decorator
