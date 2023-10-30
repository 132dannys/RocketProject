from django.db import models

from rocket.apps.common.models.core_model import CoreModel


class Contact(CoreModel):
    email = models.EmailField()
    chain_object = models.OneToOneField("objects.ChainObject", related_name="contact", on_delete=models.CASCADE)

    def __str__(self):
        return self.email
