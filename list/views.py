from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Load, Driver, Broker, Disp
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView, CreateView, DeleteView


class LoadListView(ListView):
    model = Load
    template_name = "list/load_list.html"
    context_object_name = "loads"
    paginate_by = 20
    ordering = ['id']

    def get_queryset(self):
        #basic search (AI suggested to optimize it)
        queryset = super().get_queryset().select_related('driver', 'broker', 'disp')

        #getting parameters from url (GET request)
        ref_query = self.request.GET.get('ref')
        date_query = self.request.GET.get('date')
        driver_id = self.request.GET.get('driver')
        broker_id = self.request.GET.get('broker')
        disp_id = self.request.GET.get('disp')

        #applying filters
        if ref_query:
            queryset = queryset.filter(ref_number__icontains=ref_query)

        if date_query:
            queryset = queryset.filter(booked_on=date_query)

        if driver_id:
            queryset = queryset.filter(driver_id=driver_id)

        if broker_id:
            queryset = queryset.filter(broker_id=broker_id)

        if disp_id:
            queryset = queryset.filter(disp_id=disp_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #lists for dropdowns
        context['drivers'] = Driver.objects.all().order_by('name')
        context['brokers'] = Broker.objects.all().order_by('name')
        context['disps'] = Disp.objects.all().order_by('name')

        #getting back chosen parameters from url
        context['current_ref'] = self.request.GET.get('ref', '')
        context['current_date'] = self.request.GET.get('date', '')
        context['current_driver'] = int(self.request.GET.get('driver') or 0)
        context['current_broker'] = int(self.request.GET.get('broker') or 0)
        context['current_disp'] = int(self.request.GET.get('disp') or 0)

        return context


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


class DispCreateView(CreateView):
    model = Disp
    template_name = "list/load_form.html"
    fields = ['name']
    success_url = reverse_lazy('load_list')
    extra_context = {'title': 'Add New Disp'}


class DriverCreateView(CreateView):
    model = Driver
    template_name = "list/load_form.html"
    fields = ['name', 'pay_type', 'driver_percent', 'driver_per_mile',
              'truck_number', 'dims', 'payload'
              ]
    success_url = reverse_lazy('load_list')
    extra_context = {'title': 'Add New Driver'}


class LoadEditView(UpdateView):
    model = Load
    template_name = "list/load_form.html"
    fields = [
        'ref_number', 'booked_on',
        'broker', 'driver', 'disp',
        'rate', 'miles', 'disp_percent',
        'rc', 'bol', 'pod',
        'drivers_payout_final',
        'dispatcher_payout_final',
        'company_profit_final',
    ]
    success_url = reverse_lazy('load_list')

    def form_valid(self, form):
        obj = form.instance

        if 'drivers_payout_final' not in form.changed_data:
            obj.drivers_payout_final = None

        if 'dispatcher_payout_final' not in form.changed_data:
            obj.dispatcher_payout_final = None

        if 'company_profit_final' not in form.changed_data:
            obj.company_profit_final = None

        return super().form_valid(form)


class BrokerCreateView(CreateView):
    model = Broker
    template_name = "list/load_form.html"
    fields = ['name', 'notes']
    extra_context = {'title': 'Add New Broker'}
    success_url = reverse_lazy('load_list')


class LoadDeleteView(DeleteView):
    model = Load
    template_name = "list/load_confirm_delete.html"
    success_url = reverse_lazy('load_list')
