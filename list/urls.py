from django.urls import path
from .views import LoadListView, LoadUpdateView

urlpatterns = [
    path('', LoadListView.as_view(), name='load_list'),
    path('load/<int:pk>/upload/', LoadUpdateView.as_view(), name='load_upload'),
]