from django.db import models

from rocket.apps.common.models.core_model import CoreModel


class Product(CoreModel):
    name = models.CharField(max_length=127)
    model = models.CharField(max_length=127)
    release = models.DateField()

    def __str__(self):
        return self.name
