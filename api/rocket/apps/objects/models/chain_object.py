from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from rocket.apps.common.models.core_model import CoreModel
from rocket.apps.objects.choices import PlaceType


class ChainObject(CoreModel):
    name = models.CharField(max_length=50, unique=True)
    contact = models.OneToOneField(
        "contacts.Contact", related_name="chain_object", null=True, on_delete=models.SET_NULL
    )
    employees = models.ManyToManyField(User, blank=True)
    type = models.PositiveSmallIntegerField(choices=PlaceType.choices, default=PlaceType.factory)
    supplier = models.ForeignKey("self", related_name="parent", null=True, blank=True, on_delete=models.SET_NULL)
    products = models.ManyToManyField("products.Product", related_name="chain_objects", default=None, blank=True)
    dept = models.DecimalField(default=0, max_digits=100, decimal_places=2)

    def clean(self):
        """
        Method to validate Supplier hierarchy. Supplier must be less than the Type in the Chain hierarchy.
        """
        if self.supplier is None:
            pass
        elif self.type <= self.supplier.type:
            raise ValidationError({"supplier": "Supplier must be less than the Type in the Chain hierarchy."})

    def __str__(self):
        return self.name
