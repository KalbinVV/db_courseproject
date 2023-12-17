from flask import request

import data.utils
import models
from security import should_be_authed, get_user, should_be_owner_of_housing


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

    address = models.Addresses(house_number=str(house_number),
                               street_id=street_id)

    comforts = _parse_comforts()

    if department_number != '':
        address.department_number = department_number

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

    return {'successful': True}


def export_data():
    data.utils.export_data()

    return 'exported'


def get_streets_by_like_name():
    settlement_id = request.args.get('settlement_id')
    term = request.args.get('search')

    search = "%{}%".format(term)

    streets = [{'text': street.name,
                'id': street.id}
               for street in models.Streets.query
               .filter(models.Streets.name.like(search),
                       models.Streets.settlement_id == int(settlement_id)).all()]

    return streets
