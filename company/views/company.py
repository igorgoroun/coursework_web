from django.shortcuts import render, reverse
from django.http import HttpRequest, HttpResponseRedirect
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from company.models import Employee, Company, CompanyForm


import logging

_logger = logging.getLogger(__name__)


class CompanyView(LoginRequiredMixin, View):

    http_method_names = ['get', 'post']
    form_class = CompanyForm
    initial_data = {}
    template_name = 'company_form.html'

    def get(self, request, *args, **kwargs):
        """
        :param request:
        :type request HttpRequest
        """
        user = Employee.objects.get(request.user)
        form = self.form_class(initial=user.company if user.company else self.initial_data)
        _logger.debug(f"Load form {str(form)}")
        return render(request, template_name=self.template_name, context={'form': form})

    def post(self, request, *args, **kwargs):
        """
        :param request:
        :type request HttpRequest
        """
        form = self.form_class(request.POST)
        _logger.debug(f'Got form data: {request.POST}')
        if form.is_valid():
            _logger.debug('Form is valid')
            return HttpResponseRedirect('homepage')

        return render(request, self.template_name, {'form': form})


class CompanyUpdateView(UpdateView):
    template_name_suffix = '_form'
    model = Company
    fields = [
        'name_last',
        'name_first',
        'name_middle',
        'address_line_1',
        'address_line_2',
        'address_line_3',
        'tel_number',
        'tel_fax',
        'itn',
        'reg'
    ]
    success_url = '/'


class CompanyCreateView(LoginRequiredMixin, CreateView):
    template_name_suffix = '_form'
    model = Company
    fields = [
        'name_last',
        'name_first',
        'name_middle',
        'address_line_1',
        'address_line_2',
        'address_line_3',
        'tel_number',
        'tel_fax',
        'itn',
        'reg'
    ]
    success_url = '/'

    def form_valid(self, form):
        _logger.info("Run form_valid")
        self.object = form.save()
        user = self.request.user
        user.company = self.object
        user.save()
        return HttpResponseRedirect(reverse('setup_dashboard'))

