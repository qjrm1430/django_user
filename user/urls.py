from django.urls import path

from .views import join_user, login_user, logout_user

urlpatterns = [
    path("login/", login_user, name="login-user"),
    path("join/", join_user, name="join-user"),
    path("logout/", logout_user, name="logout-user"),
]
