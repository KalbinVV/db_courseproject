import json

from flask import render_template, request

import models
from utils.comforts_utils import get_comforts
from utils.housings_utils import get_housings_types
from utils.locations_utils import get_countries


def search_page():
    return render_template('search.html', housings_types=get_housings_types(),
                           comforts=get_comforts(),
                           countries=get_countries())


def get_search_result():
    def _parse_comforts():
        comforts_list = []

        for i in range(int(request.args.get('comforts_amount'))):
            comfort_id = int(request.args.get(f'comforts[{i}][id]'))
            comfort_value = int(request.args.get(f'comforts[{i}][value]'))

            comforts_list.append({'id': comfort_id, 'value': comfort_value})

        return comforts_list

    housings_types = tuple(map(int, json.loads(request.args.get('housings_types'))))
    settlement_id = request.args.get('settlement_id')
    street_id = request.args.get('street_id')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')
    comforts = _parse_comforts()

    records = models.Records.query \
        .filter(models.Addresses.settlement_id == int(settlement_id)) \
        .filter(models.Records.price >= int(min_price), models.Records.price <= int(max_price))

    if street_id is not None and street_id != '':
        records = records.filter(models.Addresses.street_id == int(street_id))

    records = records.with_entities(models.Records).all()

    parsed_records = []

    for record in records:
        housing = models.Housings.query.filter_by(id=record.housing_id).first()
        housing_type = models.HousingsTypes.query.filter_by(id=housing.housing_type_id).first()

        if housing_type.id not in housings_types:
            continue

        parsed_records.append({'id': record.id,
                               'title': record.title,
                               'description': record.description,
                               'price': record.price,
                               'icon': housing_type.icon,
                               'type': housing_type.name})

    return parsed_records
