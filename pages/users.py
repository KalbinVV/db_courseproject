from flask import request

from security import is_user_authed, get_user


def users_me() -> dict:
    if not is_user_authed():
        return {"user_id": -1, "is_quest": True}

    user = get_user()

    return {"user_id": user.id, "is_quest": False}
