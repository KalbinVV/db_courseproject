import models


def get_users():
    users = models.User.query.all()

    return [{'id': user.id,
             'username': user.username}
            for user in users]
