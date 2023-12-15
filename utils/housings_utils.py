import models


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
