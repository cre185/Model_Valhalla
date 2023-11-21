from django.urls import path

from . import views

urlpatterns = [
    path("create", views.createView.as_view(), name="create"),
    path("upload", views.uploadView.as_view(), name="upload"),
    path("delete/<int:id>", views.deleteView.as_view(), name="delete"),
    path("update/<int:id>", views.updateView.as_view(), name="update"),
    path("retrieve/<int:id>", views.retrieveView.as_view(), name="retrieve"),
    path("list", views.listView.as_view(), name="list"),
]
