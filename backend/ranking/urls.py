from django.urls import path

from . import views

urlpatterns = [
    path('update', views.updateView.as_view(), name='update'),
    path('list', views.listView.as_view(), name='list'),
    path('retrieve', views.retrieveView.as_view(), name='retrieve'),
    path('clear', views.clearView.as_view(), name='clear'),
    path('comment', views.commentView.as_view(), name='comment'),
    path('dataset_comment/<int:id>', views.datasetCommentView.as_view(), name='dataset_comment'),
    path('llm_comment/<int:id>', views.llmCommentView.as_view(), name='llm_comment'),
    path('like_dataset_comment', views.likeDCommentView.as_view(), name='like_dataset_comment'),
    path('like_llm_comment', views.likeLCommentView.as_view(), name='like_llm_comment'),
]