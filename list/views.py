from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Load


class LoadListView(ListView):
    model = Load
    template_name = "list/load_list.html"
    context_object_name = "loads"
    paginate_by = 10
    ordering = ['-booked on']


class LoadUpdateView(DetailView):
    model = Load
    template_name = "list/load_form"
    fields = ["rc", "bol", "pod"]
    success_url = reverse_lazy('load_list')
