from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Load
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView


class LoadListView(ListView):
    model = Load
    template_name = "list/load_list.html"
    context_object_name = "loads"
    paginate_by = 10
    ordering = ['-booked_on']


class LoadUpdateView(UpdateView):
    model = Load
    template_name = "list/load_form.html"
    fields = ["rc", "bol", "pod"]
    success_url = reverse_lazy('load_list')

class LoadCreateView(CreateView):
    model = Load
    template_name = "list/load_form.html"
    fields = [
        'ref_number', 'booked_on',
        'broker', 'driver', 'disp',
        'rate', 'miles', 'disp_percent',
        'rc', 'bol'
    ]
    success_url = reverse_lazy('load_list')
