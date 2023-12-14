from flask import render_template

from security import should_be_authed


@should_be_authed
def my_profile():
    return render_template('profile.html')
