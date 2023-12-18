import datetime
import json

from sqlalchemy import func, desc

import models


def get_landlord_logs(user_id: int):
    logs: list[models.History] = models.History.query\
        .filter_by(owner_id=user_id) \
        .order_by(desc(models.History.id)) \
        .with_entities(models.History.price,
                       models.History.renter_id,
                       models.History.housing_id,
                       models.History.price,
                       models.History.rent_start,
                       models.History.rent_end,
                       models.History.id).all()

    parsed_logs = []

    for log in logs:
        renter = models.User.query.filter_by(id=log.renter_id).first()
        housing = models.Housings.query.filter_by(id=log.housing_id).first()

        parsed_logs.append({
            'id': log.id,
            'price': log.price,
            'housing_name': housing.name,
            'housing_id': log.housing_id,
            'rent_start': log.rent_start,
            'rent_end': log.rent_end,
            'renter_name': renter.username if renter else None
        })

    return parsed_logs


def get_renter_logs(user_id: int):
    logs: list[models.History] = models.History.query\
        .filter_by(renter_id=user_id) \
        .order_by(desc(models.History.id)) \
        .with_entities(models.History.price,
                       models.History.owner_id,
                       models.History.housing_id,
                       models.History.price,
                       models.History.rent_start,
                       models.History.rent_end,
                       models.History.id).all()

    parsed_logs = []

    for log in logs:
        owner = models.User.query.filter_by(id=log.owner_id).first()
        housing = models.Housings.query.filter_by(id=log.housing_id).first()

        parsed_logs.append({
            'id': log.id,
            'price': log.price,
            'housing_name': housing.name,
            'housing_id': log.housing_id,
            'rent_start': log.rent_start,
            'rent_end': log.rent_end,
            'owner_name': owner.username if owner else None
        })

    return parsed_logs


def get_landlord_logs_by_dates(user_id: int, date_start: datetime.datetime, date_end: datetime.datetime):
    logs: list[models.History] = models.History.query\
        .filter_by(owner_id=user_id)\
        .filter(models.History.rent_start >= date_start, models.History.rent_start <= date_end)\
        .order_by(desc(models.History.id))\
        .with_entities(models.History.price,
                       models.History.renter_id,
                       models.History.housing_id,
                       models.History.price,
                       models.History.rent_start,
                       models.History.rent_end,
                       models.History.id).all()

    final_sum = 0

    parsed_logs = []

    for log in logs:
        renter = models.User.query.filter_by(id=log.renter_id).first()
        housing = models.Housings.query.filter_by(id=log.housing_id).first()

        parsed_logs.append({
            'id': log.id,
            'price': log.price,
            'housing_name': housing.name,
            'housing_id': log.housing_id,
            'rent_start': log.rent_start,
            'rent_end': log.rent_end,
            'renter_name': renter.username if renter else None
        })

        final_sum += log.price

    return {'sum': final_sum,
            'items': parsed_logs}
