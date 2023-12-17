from functools import wraps
from typing import Callable

import jwt
from flask import Response, make_response, request

import models


def has_token() -> bool:
    return 'token' in request.cookies


def is_user_authed():
    if not has_token():
        return False

    try:
        decode_token()

        return True
    except (Exception, ):
        return False


def create_token(user: models.User) -> str:
    encoded_jwt = jwt.encode({"user_id": user.id}, "secret", algorithm="HS256")

    return encoded_jwt


def decode_token() -> int:
    jwt_token = request.cookies.get('token')

    decoded_jwt = jwt.decode(jwt_token, "secret", algorithms=["HS256"])

    return int(decoded_jwt['user_id'])


def get_user() -> models.User:
    return models.User.query.filter_by(id=decode_token()).first_or_404()


def should_be_authed(function: Callable) -> Callable:
    @wraps(function)
    def decorator(*args, **kwargs) -> Response | str:
        if not is_user_authed():
            return make_response("Вы не авторизированы!", 400)

        return function(*args, **kwargs)

    return decorator


def should_be_owner_of_housing(function):
    @wraps(function)
    def decorator(*args, **kwargs):
        housing_id = request.args.get('housing_id')

        if housing_id is None:
            housing_id = request.form.get('housing_id')

        housing_id = int(housing_id)

        user = get_user()

        housing: models.Housings = models.Housings.query.filter_by(id=housing_id).first_or_404()

        if housing.owner_id != user.id:
            return 400, "Вы должны быть владельцем данной недвижимости!"

        return function(*args, **kwargs)

    return decorator
