from typing import Optional

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


def parse_address_by_id(address_id: int) -> dict:
    address = models.Addresses.query.filter_by(id=address_id).first_or_404()

    return parse_address(address)


def parse_address(address: models.Addresses) -> dict:
    street: models.Streets = models.Streets.query.filter_by(id=address.street_id).first()
    settlement: models.Settlements = models.Settlements.query.filter_by(id=street.settlement_id).first()
    country = models.Countries.query.filter_by(id=settlement.country_id).first()

    return {'street': street,
            'settlement': settlement,
            'country': country,
            'house_number': address.house_number,
            'department_number': address.department_number}


def parse_address_by_street_id(street_id) -> dict:
    street: models.Streets = models.Streets.query.filter_by(id=street_id).first()
    settlement: models.Settlements = models.Settlements.query.filter_by(id=street.settlement_id).first()
    country = models.Countries.query.filter_by(id=settlement.country_id).first()

    return {'street': street,
            'settlement': settlement,
            'country': country}


def is_location_exists(street_id: int, house_number: str, department_number: Optional[str]) -> bool:
    address_args = parse_address_by_street_id(street_id)

    if models.Addresses.query.filter_by(street_id=int(street_id),
                                        country_id=int(address_args['country'].id),
                                        house_number=house_number,
                                        department_number=department_number).count() > 0:
        return True

    return False
