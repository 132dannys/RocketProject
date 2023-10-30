from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    chain_object = models.ForeignKey("objects.ChainObject", null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.username
