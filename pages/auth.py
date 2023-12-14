import hashlib

from flask import make_response, redirect, url_for, Response, request

import models
from helpers_decorators import redirect_to_index_if_authed, render_template_if_method
from security import should_be_authed, create_token


@should_be_authed
def logout():
    response = make_response(redirect(url_for('index')))
    response.delete_cookie('token')

    return response


@render_template_if_method('register.html', methods=['GET'])
@redirect_to_index_if_authed
def register() -> str | Response:
    user = models.User(username=request.form.get('username'),
                       hashed_password=hashlib.sha256(request.form.get('password').encode()).hexdigest(),
                       email=request.form.get('email'),
                       phone_number=request.form.get('phone_number')
                       )

    models.db.session.add(user)
    models.db.session.commit()

    token = create_token(user)

    response = make_response(redirect(url_for('index')))
    response.set_cookie('token', token)

    return response


@render_template_if_method('auth.html', methods=['GET'])
@redirect_to_index_if_authed
def auth() -> str | Response | dict:
    username = request.form.get('username')
    password = hashlib.sha256(request.form.get('password').encode()).hexdigest()

    user = models.User.query.filter_by(username=username, hashed_password=password).first()

    if user is None:
        return {"authed": False}

    token = create_token(user)

    response = make_response(redirect(url_for('index')))
    response.set_cookie('token', token)

    return response
