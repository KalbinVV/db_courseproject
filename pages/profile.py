import datetime

from flask import render_template, request, redirect

import models
from security import should_be_authed, get_user, should_be_owner_of_housing
from utils.comforts_utils import get_comforts, get_housing_comforts
from utils.housings_utils import get_housings_types, get_housings
from utils.locations_utils import get_countries, parse_address_by_id
from utils.records_utils import get_user_records


@should_be_authed
def my_profile():
    user = get_user()

    return render_template('profile.html',
                           username=user.username,
                           records=get_user_records(user.id))


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
                           housings_types=get_housings_types(),
                           comforts=get_comforts())


@should_be_authed
def view_housing():
    housing_id = int(request.args.get('housing_id'))

    housing = models.db.get_or_404(models.Housings, housing_id)

    address = parse_address_by_id(housing.address_id)

    housing_icon = models.HousingsTypes.query.filter_by(id=housing.housing_type_id).first().icon

    user = get_user()

    return render_template('view_housing.html',
                           housing=housing,
                           address=address,
                           housing_icon=housing_icon,
                           is_owner=(housing.owner_id == user.id),
                           comforts=get_housing_comforts(housing.id))


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
                               address=parse_address_by_id(housing.address_id),
                               comforts=get_housing_comforts(housing.id))
    elif request.method == 'POST':
        def _parse_comforts():
            comforts_list = []

            for i in range(int(request.form.get('comforts_amount'))):
                comfort_id = int(request.form.get(f'comforts[{i}][id]'))
                comfort_value = int(request.form.get(f'comforts[{i}][value]'))

                comforts_list.append({'id': comfort_id, 'value': comfort_value})

            return comforts_list

        housing_id = int(request.form.get('housing_id'))
        housing = models.db.get_or_404(models.Housings, housing_id)
        comforts = _parse_comforts()

        name = request.form.get('name')
        description = request.form.get('description')

        housing.name = name
        housing.description = description
        housing.updated_at = datetime.datetime.utcnow()

        models.ComfortsAssociationTable.query.filter_by(housing_id=housing_id).delete()
        models.db.session.commit()

        for comfort in comforts:
            comfort_association = models.ComfortsAssociationTable(comfort_id=comfort['id'],
                                                                  housing_id=housing.id,
                                                                  value=comfort['value'])

            models.db.session.add(comfort_association)
            models.db.session.commit()

    return redirect('/my_housings')


@should_be_authed
def create_record():
    if request.method == 'GET':
        housing_id = request.args.get('housing_id')
        return render_template("create_record.html", comforts=get_comforts(),
                               housing_id=housing_id)
    else:
        housing_id = int(request.form.get('housing_id'))
        title = request.form.get('title')
        description = request.form.get('description')
        price = request.form.get('price')

        if models.Records.query.filter_by(housing_id=housing_id).scalar():
            return 400, "Record with this house already exists!"

        record = models.Records(title=title,
                                housing_id=housing_id,
                                description=description,
                                price=price,
                                created_time=datetime.datetime.utcnow(),
                                updated_time=datetime.datetime.utcnow())

        models.db.session.add(record)
        models.db.session.commit()

        return 'successful'


@should_be_authed
def view_record():
    record_id = request.args.get('record_id')

    return render_template('view_record.html',
                           record=models.db.get_or_404(models.Records, int(record_id)))
