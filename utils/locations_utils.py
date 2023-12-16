import models


def get_settlements():
    settlements = models.Settlements.query.all()

    return [{'name': settlement.name,
             'id': settlement.id}
            for settlement in settlements]


def get_countries():
    countries = models.Countries.query.all()

    return [{'name': country.name,
             'id': country.id}
            for country in countries]
