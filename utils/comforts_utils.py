import models


def get_comforts():
    comforts: list[models.Comforts] = models.Comforts.query.all()

    parsed_comforts = []

    for comfort in comforts:
        unit_id = comfort.unit_id

        unit: models.Units = models.db.get_or_404(models.Units, unit_id)

        parsed_comforts.append({
            "name": comfort.name,
            "description": comfort.description,
            "unit": unit.name,
            "unit_short": unit.short_name,
            "min": comfort.min_value,
            "max": comfort.max_value,
            "id": comfort.id
        })

    return parsed_comforts


def get_housing_comforts(housing_id: int):
    association_comforts: list[models.ComfortsAssociationTable] = models.ComfortsAssociationTable\
        .query.filter_by(housing_id=housing_id).all()

    comforts = []

    for assoc_comfort in association_comforts:
        comfort: models.Comforts = models.Comforts.query.filter_by(id=assoc_comfort.comfort_id).first()
        unit = models.db.get_or_404(models.Units, comfort.unit_id)

        comforts.append({
            "name": comfort.name,
            "description": comfort.description,
            "unit": unit.name,
            "unit_short": unit.short_name,
            "value": assoc_comfort.value,
            "id": comfort.id,
            "min": comfort.min_value,
            "max": comfort.max_value
        })

    return comforts
