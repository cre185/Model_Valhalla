from django.urls import path

from . import views

urlpatterns = [
    path('create', views.createView.as_view(), name='create'),
    path('delete/<int:id>', views.deleteView.as_view(), name='delete'),
    path('testing', views.testingView.as_view(), name='testing'),
    path('update/<int:id>', views.updateView.as_view(), name='update'),
    path('retrieve/<int:id>', views.retrieveView.as_view(), name='retrieve'),
    path('list', views.listView.as_view(), name='list'),
    path('battle_match', views.battleMatchView.as_view(), name='battle_match'),
    path('generate', views.generateView.as_view(), name='generate'),
    path('battle_result', views.battleResultView.as_view(), name='battle_result'),
]