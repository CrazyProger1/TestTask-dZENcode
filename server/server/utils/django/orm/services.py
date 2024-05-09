from django.db import models


def get_all_objects(model: type[models.Model]) -> models.QuerySet[models.Model]:
    return model.objects.all()


def count_objects(model: type[models.Model], *fargs, **fkwargs) -> int:
    return model.objects.filter(*fargs, **fkwargs).count()


def get_object_or_none(model: type[models.Model], *fargs, **fkwargs) -> models.Model:
    try:
        return model.objects.get(*fargs, **fkwargs)
    except model.DoesNotExist:
        return None


def get_or_create_object(model: type[models.Model], **fkwargs) -> models.Model:
    return model.objects.get_or_create(**fkwargs)[0]
