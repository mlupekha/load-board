from django.urls import path
from .views import (
    LoadListView, LoadUpdateView, LoadCreateView, LoadEditView, LoadDeleteView,
    DriverCreateView, BrokerCreateView, DispCreateView
)

urlpatterns = [
    path('', LoadListView.as_view(), name='load_list'),
    path('load/<int:pk>/upload/', LoadUpdateView.as_view(), name='load_upload'),
    path('load/add/', LoadCreateView.as_view(), name='load_add'),
    path('load/<int:pk>/edit/', LoadEditView.as_view(), name='load_edit'),
    path('load/<int:pk>/delete/', LoadDeleteView.as_view(), name='load_delete'),
    path('driver/add/', DriverCreateView.as_view(), name='driver_add'),
    path('broker/add/', BrokerCreateView.as_view(), name='broker_add'),
    path('disp/add/', DispCreateView.as_view(), name='disp_add'),
]