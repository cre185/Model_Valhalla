from django.urls import path

from . import views

urlpatterns = [
    path('update', views.updateView.as_view(), name='update'),
    path('list', views.listView.as_view(), name='list'),
    path('retrieve', views.retrieveView.as_view(), name='retrieve'),
    path('clear', views.clearView.as_view(), name='clear'),
]