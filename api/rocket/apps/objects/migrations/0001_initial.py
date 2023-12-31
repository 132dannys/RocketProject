# Generated by Django 4.2.6 on 2023-11-02 08:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("contacts", "0001_initial"),
        ("products", "0002_alter_product_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="ChainObject",
            fields=[
                ("uuid", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created", models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="created")),
                ("updated", models.DateTimeField(auto_now=True, verbose_name="updated")),
                ("name", models.CharField(max_length=50, unique=True)),
                (
                    "type",
                    models.PositiveSmallIntegerField(
                        choices=[(0, "Factory"), (1, "Distributor"), (2, "Dealer"), (3, "Retail"), (4, "Entrepreneur")],
                        default=0,
                    ),
                ),
                ("debt", models.DecimalField(decimal_places=2, default=0, max_digits=100)),
                (
                    "contact",
                    models.OneToOneField(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="chain_object",
                        to="contacts.contact",
                    ),
                ),
                ("employees", models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
                (
                    "products",
                    models.ManyToManyField(
                        blank=True, default=None, related_name="chain_objects", to="products.product"
                    ),
                ),
                (
                    "supplier",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="parent",
                        to="objects.chainobject",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
