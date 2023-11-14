from django.urls import path

from . import views

urlpatterns = [
    path('create', views.createView.as_view(), name='create'),
    path('delete/<int:id>', views.deleteView.as_view(), name='delete'),
    path('testing', views.testingView.as_view(), name='testing'),
]