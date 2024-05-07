from django.db import models


def get_all_objects(model: type[models.Model]) -> models.QuerySet[models.Model]:
    return model.objects.all()
