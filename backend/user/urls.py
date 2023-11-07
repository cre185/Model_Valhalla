from django.urls import path
from . import views

urlpatterns = [
    path("login", views.loginView.as_view(), name="login"),
    path("login_with_verify_code", views.login_with_verify_codeView.as_view(), name="login_with_verify_code"),
    path("send_message", views.send_messageView.as_view(), name="send_message"),
    path("verify_code", views.verify_codeView.as_view(), name="verify_code"),
    path("register", views.registerView.as_view(), name="register"),
    path("logout", views.logoutView.as_view(), name="logout"),
    path("send_email", views.send_emailView.as_view(), name="send_email"),
]