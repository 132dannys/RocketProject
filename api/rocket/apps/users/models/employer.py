from django.db import models
from django.contrib.auth.models import User

from rocket.apps.common.models.core_model import CoreModel


class Employer(CoreModel):
    name = models.CharField(max_length=127)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chain_object = models.ForeignKey("objects.ChainObject", null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name
