from decimal import Decimal

import pytest
from django.core import mail

from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.exceptions import ErrorDetail

from rocket.apps.objects.choices import PlaceType
from rocket.apps.objects.serializers import ChainObjectListSerializer
from rocket.apps.objects.models import ChainObject
from rocket.apps.contacts.models import Contact

from tests.test_products import first_product, second_product, third_product


@pytest.fixture(autouse=True)
def celery_setup(settings):
    settings.CELERY_TASK_ALWAYS_EAGER = True


@pytest.fixture(autouse=True)
def email_backend_setup(settings):
    settings.EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"


@pytest.fixture
def user():
    return User.objects.create_user(username="user", password="test_pass", email="example@gmail.com")


@pytest.fixture
def first_contact():
    return Contact.objects.create(
        email="first_email@example.com", country="FirstCountry", city="FirstCity", street="FirstStreet", building="1"
    )


@pytest.fixture
def second_contact():
    return Contact.objects.create(
        email="second_email@example.com",
        country="SecondCountry",
        city="SecondCity",
        street="SecondStreet",
        building="2",
    )


@pytest.fixture
def third_contact():
    return Contact.objects.create(
        email="third_email@example.com", country="ThirdCountry", city="ThirdCity", street="ThirdStreet", building="3"
    )


@pytest.fixture
def fourth_contact():
    return Contact.objects.create(email="user@example.com", country="user", city="user", street="user", building="user")


@pytest.fixture
def first_object(first_contact, first_product, second_product, third_product):
    obj = ChainObject.objects.create(name="Factory", contact=first_contact, type=PlaceType.factory)
    obj.products.set([first_product, second_product])
    return obj


@pytest.fixture
def second_object(second_contact, first_product, third_product, first_object):
    obj = ChainObject.objects.create(
        name="Distributor", contact=second_contact, type=PlaceType.distributor, supplier=first_object, debt=532
    )
    obj.products.set([first_product, third_product])
    return obj


@pytest.fixture
def third_object(third_contact, third_product, second_object):
    obj = ChainObject.objects.create(
        name="Retail", contact=third_contact, type=PlaceType.retail, supplier=second_object, debt=150
    )
    obj.products.set([third_product])
    return obj


@pytest.fixture
def secure_object(user, fourth_contact, third_product):
    obj = ChainObject.objects.create(name="UserFactory", contact=fourth_contact, type=PlaceType.factory, debt=0)
    obj.products.set([third_product])
    obj.employees.set([user])
    return obj


@pytest.mark.django_db
def test_object_list(client, user, first_object, second_object, third_object):
    client.force_login(user)
    url = reverse("api-v1-objects:object-list")
    expected_data = ChainObjectListSerializer([second_object, first_object, third_object], many=True).data
    response = client.get(url)
    assert response.status_code == 200
    assert response.data["results"] == expected_data


@pytest.mark.django_db
def test_object_create(client, user):
    client.force_login(user)
    url = reverse("api-v1-objects:object-list")
    data = {
        "name": "string",
        "type": 0,
        "debt": 0,
        "contact": {
            "email": "user@example.com",
            "country": "string",
            "city": "string",
            "street": "string",
            "building": "string",
        },
    }
    response = client.post(url, data=data, content_type="application/json")
    assert response.status_code == 201


@pytest.mark.django_db
def test_object_put(client, user, first_object, first_product):
    client.force_login(user)
    url = reverse("api-v1-objects:object-detail", args=[first_object.uuid])
    data = {
        "name": "string",
        "type": 0,
        "supplier": None,
        "products": [first_product.uuid],
        "employees": [user.id],
        "contact": {
            "email": "user@example.com",
            "country": "string",
            "city": "string",
            "street": "string",
            "building": "string",
        },
    }
    expected_data = {
        "uuid": f"{first_object.uuid}",
        "name": "string",
        "type": 0,
        "supplier": None,
        "products": [first_product.uuid],
        "employees": [user.id],
        "debt": Decimal("0.00"),
        "contact": {
            "email": "user@example.com",
            "country": "string",
            "city": "string",
            "street": "string",
            "building": "string",
        },
        "created": first_object.created,
    }
    response = client.put(url, data=data, content_type="application/json")
    assert response.status_code == 200
    assert response.data == expected_data


@pytest.mark.django_db
def test_object_patch(client, user, first_object, first_product):
    client.force_login(user)
    url = reverse("api-v1-objects:object-detail", args=[first_object.uuid])
    data = {
        "products": [first_product.uuid],
        "employees": [user.id],
        "contact": {
            "email": "user@example.com",
            "country": "string",
            "city": "string",
            "street": "string",
            "building": "string",
        },
    }
    expected_data = {
        "uuid": f"{first_object.uuid}",
        "name": first_object.name,
        "type": first_object.type,
        "supplier": first_object.supplier,
        "products": [first_product.uuid],
        "employees": [user.id],
        "debt": first_object.debt,
        "contact": {
            "email": "user@example.com",
            "country": "string",
            "city": "string",
            "street": "string",
            "building": "string",
        },
        "created": first_object.created,
    }
    response = client.patch(url, data=data, content_type="application/json")
    assert response.status_code == 200
    assert response.data == expected_data


@pytest.mark.django_db
def test_object_statistic(client, user, first_object, second_object, third_object):
    client.force_login(user)
    url = reverse("api-v1-objects:object-object-statistic")
    response = client.get(url)
    expected_data = ChainObjectListSerializer([second_object], many=True).data
    assert response.status_code == 200
    assert response.data == expected_data


@pytest.mark.django_db
def test_send_email(client, user, first_object):
    client.force_login(user)
    data = {"uuid": first_object.uuid}
    url = reverse("api-v1-objects:object-send-email")
    response = client.post(url, data=data)
    assert response.status_code == 200
    assert mail.outbox[0].body == "Here you QR Code with Object Contact information!"
    assert mail.outbox[0].subject == "QRCode of Object"
    assert mail.outbox[0].to == [user.email]


@pytest.mark.django_db
def test_object_delete(client, user, first_object):
    client.force_login(user)
    url = reverse("api-v1-objects:object-detail", args=[first_object.uuid])
    response = client.delete(url)
    assert response.status_code == 204


@pytest.mark.django_db
def test_secure_route(client, user, secure_object):
    client.force_login(user)
    url = reverse("api-v1-objects:secure_object-list")
    expected_data = ChainObjectListSerializer([secure_object], many=True).data
    response = client.get(url)
    assert response.status_code == 200
    assert response.data == expected_data


@pytest.mark.django_db
def test_permission(client, user):
    url = reverse("api-v1-objects:object-list")
    response = client.get(url)
    assert response.status_code == 401
    assert response.data == {
        "detail": ErrorDetail(string="Authentication credentials were not provided.", code="not_authenticated")
    }
