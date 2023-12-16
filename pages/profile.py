import datetime

from flask import render_template, request, redirect

import models
from security import should_be_authed, get_user, should_be_owner_of_housing
from utils.housings_utils import get_housings_types, get_housings
from utils.locations_utils import get_countries, parse_address_by_id


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


@should_be_owner_of_housing
@should_be_authed
def view_housing():
    housing_id = int(request.args.get('housing_id'))

    housing = models.db.get_or_404(models.Housings, housing_id)

    address = parse_address_by_id(housing.address_id)

    housing_icon = models.HousingsTypes.query.filter_by(id=housing.housing_type_id).first().icon

    return render_template('view_housing.html', housing=housing, address=address, housing_icon=housing_icon)


@should_be_owner_of_housing
@should_be_authed
def remove_housing():
    housing_id = int(request.args.get('housing_id'))

    housing = models.db.get_or_404(models.Housings, housing_id)

    models.db.session.delete(housing)
    models.db.session.commit()

    return redirect('/my_housings')


@should_be_owner_of_housing
@should_be_authed
def change_housing():
    if request.method == 'GET':
        housing_id = int(request.args.get('housing_id'))
        housing = models.db.get_or_404(models.Housings, housing_id)

        return render_template('change_housing.html',
                               housing=housing,
                               housing_type=models.db.get_or_404(models.HousingsTypes, housing.housing_type_id),
                               address=parse_address_by_id(housing.address_id))
    elif request.method == 'POST':
        housing_id = int(request.form.get('housing_id'))
        housing = models.db.get_or_404(models.Housings, housing_id)

        name = request.form.get('name')
        description = request.form.get('description')

        housing.name = name
        housing.description = description
        housing.updated_at = datetime.datetime.utcnow()

        models.db.session.commit()

    return redirect('/my_housings')
