from flask import render_template

from security import should_be_authed, get_user


@should_be_authed
def my_profile():
    return render_template('profile.html', username=get_user().username)


@should_be_authed
def my_housings():
    return render_template('my_housings.html', username=get_user().username)


@should_be_authed
def create_housing():
    return render_template('create_housing.html', username=get_user().username)
