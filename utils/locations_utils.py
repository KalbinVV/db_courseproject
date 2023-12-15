import models


def get_settlements():
    settlements = models.Settlements.query.all()

    return [{'name': settlement.name,
             'id': settlement.id}
            for settlement in settlements]
