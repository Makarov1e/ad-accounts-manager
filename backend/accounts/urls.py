"""URL routes for the accounts API."""

from rest_framework.routers import DefaultRouter

from .views import AccountViewSet

router = DefaultRouter()
router.register("accounts", AccountViewSet, basename="account")

urlpatterns = router.urls
