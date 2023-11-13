from django.urls import path

from . import views

urlpatterns = [
    path("create", views.createView.as_view(), name="create"),
    path("upload", views.uploadView.as_view(), name="upload"),
]