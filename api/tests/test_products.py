from datetime import date

import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from rocket.apps.products.models import Product
from rocket.apps.products.serializers import ProductListSerializer


@pytest.fixture
def user():
    return User.objects.create_user(username="user", password="test_pass")


@pytest.fixture
def first_product():
    return Product.objects.create(name="FirstProduct", model="FirstModel", release=date.today())


@pytest.fixture
def second_product():
    return Product.objects.create(name="SecondProduct", model="SecondModel", release=date.today())


@pytest.fixture
def third_product():
    return Product.objects.create(name="ThirdProduct", model="ThirdModel", release=date.today())


@pytest.mark.django_db
def test_product_list(client, user, first_product, second_product, third_product):
    client.force_login(user)
    url = reverse("api-v1-products:product-list")
    expected_data = ProductListSerializer([first_product, second_product, third_product], many=True).data
    response = client.get(url)
    assert response.status_code == 200
    assert response.data["results"] == expected_data


@pytest.mark.django_db
def test_product_create(client, user):
    client.force_login(user)
    url = reverse("api-v1-products:product-list")
    data = {"name": "name", "model": "model", "release": date.today()}
    response = client.post(url, data=data, content_type="application/json")
    assert response.status_code == 201


@pytest.mark.django_db
def test_product_put(client, user, first_product):
    client.force_login(user)
    url = reverse("api-v1-products:product-detail", args=[first_product.uuid])
    data = {"name": "name", "model": "model", "release": date.today()}
    expected_data = {"uuid": first_product.uuid, "name": "name", "model": "model", "release": f"{date.today()}"}
    response = client.put(url, data=data, content_type="application/json")
    assert response.status_code == 200
    assert response.data == expected_data


@pytest.mark.django_db
def test_product_patch(client, user, first_product):
    client.force_login(user)
    url = reverse("api-v1-products:product-detail", args=[first_product.uuid])
    data = {
        "name": "name",
    }
    expected_data = {
        "uuid": first_product.uuid,
        "name": "name",
        "model": first_product.model,
        "release": f"{first_product.release}",
    }
    response = client.patch(url, data=data, content_type="application/json")
    assert response.status_code == 200
    assert response.data == expected_data


@pytest.mark.django_db
def test_product_delete(client, user, first_product):
    client.force_login(user)
    url = reverse("api-v1-products:product-detail", args=[first_product.uuid])
    response = client.delete(url)
    assert response.status_code == 204
