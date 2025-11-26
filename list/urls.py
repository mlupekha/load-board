from django.urls import path
from .views import LoadListView, LoadUpdateView, LoadCreateView

urlpatterns = [
    path('', LoadListView.as_view(), name='load_list'),
    path('load/<int:pk>/upload/', LoadUpdateView.as_view(), name='load_upload'),
    path('load/add/', LoadCreateView.as_view(), name='load_add'),
]