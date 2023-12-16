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
            'id': housing_type.id
        }

    return statistics


def get_housings_types() -> list:
    housings_types: list[models.HousingsTypes] = models.HousingsTypes.query.all()

    return [{'name': housing_type.name,
             'id': housing_type.id,
             'department_number_required': housing_type.required_department_number}
            for housing_type in housings_types]


@should_be_authed
def get_housings() -> list:
    user = get_user()

    housings: list[models.HousingsTypes] = models.Housings.query.filter_by(owner_id=user.id).all()

    return [{'name': housing.name,
             'description': housing.description}
            for housing in housings]
