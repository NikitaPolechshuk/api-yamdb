from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"users", views.UserViewSet)

urlpatterns = [
    path("v1/auth/signup/", views.signup, name="signup"),
    path("v1/auth/token/", views.token, name="token"),
    path("v1/", include(router.urls)),
]
