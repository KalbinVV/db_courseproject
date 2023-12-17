import models


def get_user_records(user_id: int):
    records: list[models.Records] = models.db.session\
        .query(models.Records, models.Housings, models.HousingsTypes)\
        .filter(models.Records.housing_id == models.Housings.id)\
        .filter(models.Housings.housing_type_id == models.HousingsTypes.id)\
        .filter(models.Housings.owner_id == user_id).all()

    return records
