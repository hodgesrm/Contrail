from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from .forms import *

import requests, json

class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PriceView(FormView):
    template_name = "price.html"
    form_class = PriceForm
    success_url = reverse_lazy('price')

    def form_valid(self, form):
        data = {
            'operating_system': form.cleaned_data['operating_system'],
            'aws': form.cleaned_data['aws'],
            'gcp': form.cleaned_data['gcp'],
            'azure': form.cleaned_data['azure'],
            'region': form.cleaned_data['region'],
            'vcpus': form.cleaned_data['vcpus'],
            'memory': form.cleaned_data['memory'],
            'ecu': form.cleaned_data['ecu']
        }
        print(data)

        # call rest api
        url = settings.URL + '/api/data/'
        headers = {'content-type': 'application/json'}

        r = requests.post(url, data=json.dumps(data), headers=headers)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CompareView(TemplateView):
    template_name = "compare.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
