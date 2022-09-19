from django.urls import path
from django import urls
from apps.music_publisher import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'all-users', views.GetAllUsers,basename = 'all-users')

router.register(r'user-profile',views.UserProfileAPIView, basename = 'user-profile')

app_name = "users"

urlpatterns = [
   
]