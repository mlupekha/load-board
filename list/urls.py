from django.urls import path
from .views import LoadListView

urlpatterns = [
    path('', LoadListView.as_view(), name='load_list'),
]