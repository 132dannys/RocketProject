from django.core.exceptions import ValidationError
from django.db import models
from django.utils.datetime_safe import date

from rocket.apps.common.models.core_model import CoreModel


class Product(CoreModel):
    name = models.CharField(max_length=25)
    model = models.CharField(max_length=127)
    release = models.DateField()

    def clean(self):
        if self.release < date.today():
            raise ValidationError({"release": "Release must be a date starting from today."})

    def __str__(self):
        return self.name
