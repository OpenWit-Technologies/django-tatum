"""Urls for the user app."""
from rest_framework.routers import DefaultRouter

# from django_tatum.apps.users import views

router = DefaultRouter()
# router.register(r"all-users", views.GetAllUsers, basename="all-users")

# router.register(r"user-profile", views.UserProfileAPIView, basename="user-profile")

app_name = "users"

urlpatterns = []
