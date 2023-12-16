from flask import render_template, request

from security import should_be_authed, get_user
from utils.housings_utils import get_housings_types, get_housings
from utils.locations_utils import get_countries


@should_be_authed
def my_profile():
    return render_template('profile.html', username=get_user().username)


@should_be_authed
def my_housings():
    return render_template('my_housings.html',
                           username=get_user().username,
                           housings=get_housings())


@should_be_authed
def create_housing():
    return render_template('create_housing.html',
                           username=get_user().username,
                           countries=get_countries(),
                           housings_types=get_housings_types())
