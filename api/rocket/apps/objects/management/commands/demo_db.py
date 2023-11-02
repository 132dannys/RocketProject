from django.core.management import BaseCommand

from rocket.apps.objects.management.commands._factory import ChainObjectFactory, ProductFactory, UserFactory


class Command(BaseCommand):
    help = "Create demo database"

    def handle(self, *args, **options):
        users = []
        products = []
        for _ in range(30):
            user = UserFactory()
            user.save()
            users.append(user)
            product = ProductFactory()
            product.save()
            products.append(product)
            chain_object = ChainObjectFactory(employees=users, products=products)
            chain_object.save()
