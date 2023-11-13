from django.urls import path
from . import views

urlpatterns = [
    path("login", views.loginView.as_view(), name="login"),
    path("login_with_verify_code", views.login_with_verify_codeView.as_view(), name="login_with_verify_code"),
    path("send_message", views.send_messageView.as_view(), name="send_message"),
    path("verify_code", views.verify_codeView.as_view(), name="verify_code"),
    path("register", views.registerView.as_view(), name="register"),
    path("update/<int:id>", views.updateView.as_view(), name="update"),
    path("retrieve/<int:id>", views.retrieveView.as_view(), name="retrieve"),
    path("update_avatar", views.updateAvatarView.as_view(), name="update_avatar"),
    path("logout", views.logoutView.as_view(), name="logout"),
    path("delete/<int:id>", views.deleteView.as_view(), name="delete"),
    path("send_email", views.send_emailView.as_view(), name="send_email"),
    path("verify_email", views.verify_emailView.as_view(), name="verify_email"),
]
