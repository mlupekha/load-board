from django.urls import path
from .views import LoadListView, LoadUpdateView, LoadCreateView, LoadDeleteView, LoadEditView

urlpatterns = [
    path('', LoadListView.as_view(), name='load_list'),
    path('load/<int:pk>/upload/', LoadUpdateView.as_view(), name='load_upload'),
    path('load/add/', LoadCreateView.as_view(), name='load_add'),
    path('load/<int:pk>/delete/', LoadDeleteView.as_view(), name='load_delete'),
    path('load/<int:pk>/', LoadEditView.as_view(), name='load_edit')
]