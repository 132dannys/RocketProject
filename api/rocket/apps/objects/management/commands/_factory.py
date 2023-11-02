import datetime
import random

from django.contrib.auth.hashers import make_password
from django.utils.datetime_safe import date

import factory
from factory.fuzzy import FuzzyDate
from factory.django import DjangoModelFactory
from django.contrib.auth.models import User

from rocket.apps.contacts.models import Contact
from rocket.apps.objects.models import ChainObject
from rocket.apps.products.models import Product


class ContactFactory(DjangoModelFactory):
    class Meta:
        model = Contact

    email = factory.Faker("email")
    country = factory.Faker("country")
    city = factory.Faker("city")
    street = factory.Faker("street_name")
    building = factory.Faker("pyint", min_value=1, max_value=1000)


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Faker("name")
    model = factory.Faker("name")
    release = FuzzyDate(start_date=date.today(), end_date=date.today() + datetime.timedelta(days=30))


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = factory.Faker("email")
    password = factory.LazyFunction(lambda: make_password("pi3.1415"))


class ChainObjectFactory(DjangoModelFactory):
    class Meta:
        model = ChainObject

    name = factory.Faker("company")
    type = factory.Faker("random_element", elements=[0, 1, 2, 3, 4])
    contact = factory.SubFactory(ContactFactory)

    @factory.post_generation
    def products(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.products.add(*extracted)

    @factory.post_generation
    def employees(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.employees.add(*extracted)

    @factory.lazy_attribute
    def supplier(self):
        if self.type == 0:
            return None
        else:
            try:
                return ChainObject.objects.filter(type__lt=self.type).first()
            except ChainObject.DoesNotExist:
                return None

    @factory.lazy_attribute
    def debt(self):
        if self.type == 0:
            return 0
        else:
            return round(random.uniform(100, 10000), 2)
