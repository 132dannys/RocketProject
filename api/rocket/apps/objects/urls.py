from rest_framework import routers

from .views import ChainObjectViewSet, SecureChainObjectViewSet


router = routers.SimpleRouter()
router.register(r"objects", ChainObjectViewSet, basename="object")
router.register(r"secure_objects", SecureChainObjectViewSet, basename="secure_object")

urlpatterns = router.urls
