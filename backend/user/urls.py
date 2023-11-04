from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login, name="login"),
    path("login_with_verify_code", views.login_with_verify_code, name="login_with_verify_code"),
    path("send_message", views.send_message, name="send_message"),
    path("verify_code", views.verify_code, name="verify_code"),
    path("register", views.register, name="register"),
    path("logout", views.logout, name="logout")
]