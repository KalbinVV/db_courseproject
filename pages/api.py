from flask import request
from sqlalchemy import func

import data.utils
import models
from security import should_be_authed, get_user
from utils.locations_utils import is_location_exists

import datetime


def get_settlements_by_country():
    country_id = request.args.get('country_id')

    if country_id == '':
        return []

    settlements: list[models.Settlements] = models.Settlements.query \
        .filter_by(country_id=int(country_id)).all()

    return [{'name': settlement.name,
             'id': settlement.id,
             'type': models.SettlementsTypes.query.filter_by(id=settlement.settlement_type_id).first().name}
            for settlement in settlements]


def get_streets_by_settlement():
    settlement_id = request.args.get('settlement_id')

    if settlement_id == '':
        return []

    streets: list[models.Streets] = models.Streets.query.filter_by(settlement_id=int(settlement_id)).all()

    return [{'name': street.name,
             'id': street.id,
             'type': models.StreetsTypes.query.filter_by(id=street.street_type_id).first().name}
            for street in streets]


@should_be_authed
def add_housing():
    def _parse_comforts():
        comforts_list = []

        for i in range(int(request.form.get('comforts_amount'))):
            comfort_id = int(request.form.get(f'comforts[{i}][id]'))
            comfort_value = int(request.form.get(f'comforts[{i}][value]'))

            comforts_list.append({'id': comfort_id, 'value': comfort_value})

        return comforts_list

    user = get_user()

    name = request.form.get('name')
    description = request.form.get('description')
    street_id = request.form.get('street_id')
    house_number = request.form.get('house_number')
    department_number = request.form.get('department_number')
    housing_type_id = request.form.get('housing_type_id')

    if is_location_exists(int(street_id), str(house_number), department_number):
        return {'successful': False, 'message': 'Адрес занят!'}

    address = models.Addresses(street_id=int(street_id),
                               house_number=house_number)

    comforts = _parse_comforts()

    address.department_number = department_number if department_number else None

    models.db.session.add(address)

    models.db.session.commit()

    housing = models.Housings(owner_id=user.id,
                              name=str(name),
                              description=str(description),
                              address_id=address.id,
                              housing_type_id=int(housing_type_id))

    models.db.session.add(housing)
    models.db.session.commit()

    for comfort in comforts:
        comfort_association = models.ComfortsAssociationTable(comfort_id=comfort['id'],
                                                              housing_id=housing.id,
                                                              value=comfort['value'])

        models.db.session.add(comfort_association)
        models.db.session.commit()

    return {'successful': True, 'housing_id': housing.id}


def export_data():
    data.utils.export_data()

    return 'exported'


def get_streets_by_like_name():
    settlement_id = request.args.get('settlement_id')

    if settlement_id == '':
        return []

    term = request.args.get('search')

    search = "%{}%".format(term)

    streets = [{'text': street.name,
                'id': street.id}
               for street in models.Streets.query
               .filter(models.Streets.name.like(search),
                       models.Streets.settlement_id == int(settlement_id)).all()]

    return streets


@should_be_authed
def get_housings_rent_statistics():
    user = get_user()

    date_start = request.args.get('date_start')
    date_end = request.args.get('date_end')

    if date_start is None or date_start == '':
        date_start = datetime.datetime.today()
    else:
        date_start = datetime.datetime.strptime(date_start, '%Y-%m-%d')

    if date_end is None or date_end == '':
        date_end = datetime.datetime.today()
    else:
        date_end = datetime.datetime.strptime(date_end, '%Y-%m-%d')

    housings_statistics = models.db.session.query(func.sum(models.History.price).label('sum'),
                                                  func.avg(models.History.price).label('avg'),
                                                  models.Housings.name) \
        .filter_by(owner_id=user.id)\
        .filter(models.History.rent_start >= date_start, models.History.rent_start <= date_end)\
        .join(models.Housings).group_by(models.Housings.name).all()

    statistics = [{'name': statistic.name, 'sum': statistic.sum, 'avg': statistic.avg}
                  for statistic in housings_statistics]

    parsed_statistics = {'names': [statistic['name'] for statistic in statistics],
                         'sum_values': list(map(int, [statistic['sum'] for statistic in statistics])),
                         'avg_values': list(map(int, [statistic['avg'] for statistic in statistics]))}

    return {'source': statistics, 'parsed': parsed_statistics}
