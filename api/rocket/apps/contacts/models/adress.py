from django.db import models

from rocket.apps.common.models.core_model import CoreModel


class Address(CoreModel):
    country = models.CharField(max_length=127)
    city = models.CharField(max_length=127)
    street = models.CharField(max_length=127)
    building = models.CharField(max_length=127)
    contact = models.OneToOneField("contacts.Contact", related_name="address", on_delete=models.CASCADE)
