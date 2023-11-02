from django.core.management import BaseCommand

from rocket.apps.objects.management.commands._factory import ChainObjectFactory, ProductFactory, UserFactory


class Command(BaseCommand):
    help = "Create demo database"

    def handle(self, *args, **options):
        for _ in range(30):
            user = UserFactory()
            user.save()
            product = ProductFactory()
            product.save()
            chain_object = ChainObjectFactory()
            chain_object.save()
