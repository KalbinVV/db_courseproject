import datetime

from flask import render_template, request, redirect

import models
from security import should_be_authed, get_user, should_be_owner_of_housing
from utils.comforts_utils import get_comforts, get_housing_comforts
from utils.housings_utils import get_housings_types, get_housings
from utils.locations_utils import get_countries, parse_address_by_id
from utils.records_utils import get_user_records
from utils.users_utils import get_users


@should_be_authed
def profile():
    user_id = request.args.get('user_id')

    if user_id is None:
        user = get_user()
        visitor = get_user()
    else:
        user = models.db.get_or_404(models.User, int(user_id))
        visitor = get_user()

    return render_template('profile.html',
                           user=user,
                           visitor=visitor,
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
    else:
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

    return str(housing_id)


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
                                created_date=datetime.datetime.today(),
                                updated_time=datetime.datetime.utcnow())

        models.db.session.add(record)
        models.db.session.commit()

        return str(record.id)


@should_be_authed
def view_record():
    record_id = request.args.get('record_id')

    record = models.db.get_or_404(models.Records, int(record_id))
    housing = models.db.get_or_404(models.Housings, record.housing_id)

    user = get_user()
    is_owner = housing.owner_id == user.id

    if not is_owner and record.current_status == 'Hidden':
        return 'Объявление не найдено либо скрыто'

    return render_template('view_record.html',
                           record=record,
                           is_owner=is_owner,
                           user=models.db.get_or_404(models.User, int(housing.owner_id)))


@should_be_authed
def activate_record():
    record_id = request.args.get('record_id')

    record = models.db.get_or_404(models.Records, record_id)
    housing = models.db.get_or_404(models.Housings, record.housing_id)

    user = get_user()

    if user.id != housing.owner_id:
        return 400, 'Вы должны быть владельцем данной недвижимости!'

    record.current_status = 'Active'

    models.db.session.commit()

    return redirect(f'/view_record?record_id={record_id}')


@should_be_authed
def hide_record():
    record_id = request.args.get('record_id')

    record = models.db.get_or_404(models.Records, record_id)

    housing = models.db.get_or_404(models.Housings, record.housing_id)

    user = get_user()

    if user.id != housing.owner_id:
        return 400, 'Вы должны быть владельцем данной недвижимости!'

    record.current_status = 'Hidden'

    models.db.session.commit()

    return redirect(f'/view_record?record_id={record_id}')


@should_be_authed
def update_profile():
    phone_number = request.form.get('phone_number')
    email = request.form.get('email')

    user = get_user()
    user.phone_number = phone_number
    user.email = email

    models.db.session.commit()

    return redirect('/profile')


@should_be_authed
def update_record():
    record_id = int(request.form.get('record_id'))

    record = models.db.get_or_404(models.Records, record_id)

    housing = models.db.get_or_404(models.Housings, record.housing_id)

    user = get_user()

    if user.id != housing.owner_id:
        return 400, 'Вы должны быть владельцем данной недвижимости!'

    title = str(request.form.get('title'))
    description = str(request.form.get('description'))
    price = int(request.form.get('price'))

    record.title = title
    record.description = description
    record.price = price
    record.updated_time = datetime.datetime.utcnow()

    models.db.session.commit()

    return redirect(f'/view_record?record_id={record.id}')


@should_be_authed
def rent_housing():
    if request.method == 'GET':
        housing = models.db.get_or_404(models.Housings, request.args.get('housing_id'))

        return render_template('rent_housing.html',
                               users=get_users(),
                               housing=housing)
