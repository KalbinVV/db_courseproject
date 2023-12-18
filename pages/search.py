import datetime
import json

from flask import render_template, request
from sqlalchemy import asc, desc

import models
from main import app
from utils.comforts_utils import get_comforts
from utils.housings_utils import get_housings_types
from utils.locations_utils import get_countries


def search_page():
    selected_housing_type = request.args.get('selected_housing_type')
    selected_country = request.args.get('selected_country')

    if selected_housing_type != '' and selected_housing_type is not None:
        selected_housing_type = int(selected_housing_type)

    if selected_country != '' and selected_country is not None:
        selected_country = int(selected_country)

    return render_template('search.html', housings_types=get_housings_types(),
                           comforts=get_comforts(),
                           countries=get_countries(),
                           selected_housing_type=selected_housing_type,
                           selected_country=selected_country)


def get_search_result():
    def _parse_comforts():
        comforts_list = []

        for i in range(int(request.args.get('comforts_amount'))):
            comfort_id = int(request.args.get(f'comforts[{i}][id]'))
            comfort_value = int(request.args.get(f'comforts[{i}][value]'))

            comforts_list.append({'id': comfort_id, 'value': comfort_value})

        return comforts_list

    housings_types = list(map(int, json.loads(request.args.get('housings_types'))))
    settlement_id = request.args.get('settlement_id')
    street_id = request.args.get('street_id')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')
    date_start = request.args.get('date_start')
    date_end = request.args.get('date_end')
    comforts = _parse_comforts()

    if date_start is None or date_start == '':
        date_start = datetime.datetime.today()
    else:
        date_start = datetime.datetime.strptime(date_start, '%Y-%m-%d')

    if date_end is None or date_end == '':
        date_end = datetime.datetime.today()
    else:
        date_end = datetime.datetime.strptime(date_end, '%Y-%m-%d')

    records = models.Records.query \
        .join(models.Housings) \
        .join(models.User, models.User.id == models.Housings.owner_id) \
        .join(models.Addresses)\
        .join(models.HousingsTypes)\
        .join(models.Streets)\
        .filter(models.Records.current_status == 'Active')\
        .filter(models.Addresses.settlement_id == int(settlement_id)) \
        .filter(models.Records.price >= int(min_price), models.Records.price <= int(max_price))\
        .filter(models.Housings.housing_type_id.in_(housings_types))\
        .filter(models.Records.created_date >= date_start, models.Records.created_date <= date_end)

    if street_id is not None and street_id != '':
        records = records.filter(models.Addresses.street_id == int(street_id))

    records = records.with_entities(models.Records.id,
                                    models.Records.title,
                                    models.Records.description,
                                    models.Records.price,
                                    models.HousingsTypes.icon,
                                    models.HousingsTypes.name.label('housing_type_name'),
                                    models.Housings.id.label('housing_id'),
                                    models.Streets.name.label('street_name'),
                                    models.Addresses.house_number,
                                    models.Addresses.department_number,
                                    models.User.username,
                                    models.Records.created_date,
                                    models.Records.updated_time)\
        .order_by(asc(models.Records.price), desc(models.Records.updated_time)).all()

    parsed_records = []

    for record in records:
        housings_comforts = models.Comforts.query\
            .join(models.ComfortsAssociationTable)\
            .filter(models.ComfortsAssociationTable.housing_id == record.housing_id)\
            .order_by(asc(models.Comforts.id))\
            .with_entities(models.ComfortsAssociationTable.value.label('value')).all()

        comforts_not_suitable = False

        for i, housing_comfort in enumerate(housings_comforts):
            if housing_comfort.value < comforts[i]['value']:
                comforts_not_suitable = True
                break

        if comforts_not_suitable:
            continue

        parsed_records.append({'id': record.id,
                               'title': record.title,
                               'description': record.description,
                               'price': record.price,
                               'icon': record.icon,
                               'type': record.housing_type_name,
                               'street_name': record.street_name,
                               'house_number': record.house_number,
                               'department_number': record.department_number,
                               'username': record.username,
                               'created_data': record.created_date,
                               'updated_time': record.updated_time})

    return parsed_records
