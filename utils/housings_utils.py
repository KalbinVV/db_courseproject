from sqlalchemy import desc

import models
from security import should_be_authed, get_user


def get_housings_statistic() -> dict:
    housings_types = models.HousingsTypes.query.all()

    statistics = dict()

    for housing_type in housings_types:
        records_counts = models.Housings.query.filter_by(housing_type_id=housing_type.id).count()

        statistics[housing_type.name] = {
            'count': records_counts,
            'description': housing_type.description,
            'id': housing_type.id,
            'icon': housing_type.icon
        }

    return statistics


def get_housings_types() -> list:
    housings_types: list[models.HousingsTypes] = models.HousingsTypes.query.all()

    return [{'name': housing_type.name,
             'id': housing_type.id,
             'department_number_required': housing_type.required_department_number,
             'icon': housing_type.icon}
            for housing_type in housings_types]


@should_be_authed
def get_housings() -> list:
    user = get_user()

    housings: list[models.Housings] = models.Housings.query\
        .filter_by(owner_id=user.id).order_by(desc(models.Housings.updated_at)).all()

    parsed_housings = []

    for housing in housings:
        housing_type = models.HousingsTypes.query.filter_by(id=housing.housing_type_id).first()

        parsed_housings.append({'name': housing.name,
                                'id': housing.id,
                                'description': housing.description,
                                'type_str': housing_type.name,
                                'icon': housing_type.icon
                                })

    return parsed_housings
