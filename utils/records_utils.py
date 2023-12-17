import models


def get_user_records(user_id: int):
    records: list[models.Records] = models.db.session\
        .query(models.Records).filter(models.Housings.owner_id == user_id).all()

    return records
