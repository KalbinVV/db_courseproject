import hashlib
import json
import os.path

from flask import Flask, render_template, request, make_response, Response, redirect, url_for

import security
from models import db
import models

app = Flask(__name__,
            template_folder=os.path.abspath('./web/html'),
            static_folder=os.path.abspath('./web/static'))

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)


@app.route('/')
def index() -> str:
    return render_template('index.html')


@app.route('/users/me')
def users_me() -> str:
    if not security.is_user_authed(request):
        return json.dumps({"user_id": -1, "is_quest": True})

    user = security.get_user(request)

    return json.dumps({"user_id": user.id, "is_quest": False})


@app.route('/auth', methods=["POST", "GET"])
def auth() -> str | Response:
    if security.has_token(request):
        return redirect(url_for('index'))

    if request.method == 'GET':
        return render_template('auth.html')

    username = request.form.get('username')
    password = hashlib.sha256(request.form.get('password').encode()).hexdigest()

    user = models.User.query.filter_by(username=username, hashed_password=password).first()

    if user is None:
        return json.dumps({"authed": False})

    token = security.create_token(user)

    response = make_response(redirect(url_for('index')))
    response.set_cookie('token', token)

    return response


@app.route('/register', methods=["POST", "GET"])
def register() -> str | Response:
    if security.has_token(request):
        return redirect(url_for('index'))

    if request.method == 'GET':
        return render_template('register.html')

    user = models.User(username=request.form.get('username'),
                       hashed_password=hashlib.sha256(request.form.get('password').encode()).hexdigest(),
                       email=request.form.get('email'),
                       phone_number=request.form.get('phone_number')
                       )

    db.session.add(user)
    db.session.commit()

    token = security.create_token(user)

    response = make_response(redirect(url_for('index')))
    response.set_cookie('token', token)

    return response


@app.route('/logout')
@security.should_be_authed
def logout():
    response = make_response(redirect(url_for('index')))
    response.delete_cookie('token')

    return response


@app.route('/housings_statistics')
def housings_statistic():
    housings_types = models.HousingsTypes.query.all()

    statistics = dict()

    for housing_type in housings_types:
        records_counts = models.Housings.query.filter_by(housing_type_id=housing_type.id).count()

        statistics[housing_type.name] = {
            'count': records_counts,
            'description': housing_type.description
        }

    return json.dumps(statistics)


def main() -> None:
    with app.app_context():
        db.create_all()

    app.run()


if __name__ == "__main__":
    main()
