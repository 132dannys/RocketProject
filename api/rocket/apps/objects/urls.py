from rest_framework import routers

from .views import ChainObjectViewSet


router = routers.SimpleRouter()
router.register(r"objects", ChainObjectViewSet, basename="object")

urlpatterns = router.urls
