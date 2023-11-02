from django.db import models

from rocket.apps.common.models.core_model import CoreModel


class Contact(CoreModel):
    email = models.EmailField()
    country = models.CharField(max_length=127)
    city = models.CharField(max_length=127)
    street = models.CharField(max_length=127)
    building = models.CharField(max_length=127)

    def __str__(self):
        return self.email
