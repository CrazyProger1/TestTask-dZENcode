from django.db import models
from django import shortcuts


def get_all_objects(model: type[models.Model]) -> models.QuerySet[models.Model]:
    return model.objects.all()


def get_object_or_404(model: type[models.Model], **filters) -> models.Model:
    return shortcuts.get_object_or_404(model, **filters)
