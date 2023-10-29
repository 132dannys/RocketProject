from django.db import models
from django.utils.translation import gettext_lazy as _


class PlaceType(models.IntegerChoices):
    factory = 0, _("Factory")
    distributor = 1, _("Distributor")
    dealer = 2, _("Dealer")
    retail = 3, _("Retail")
    entrepreneur = 4, _("Entrepreneur")
