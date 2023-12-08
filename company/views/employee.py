from django.shortcuts import render, reverse
from django.http import HttpRequest, HttpResponseRedirect
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from company.models import Employee, Company, EmployeeSelfUpdateForm


import logging

_logger = logging.getLogger(__name__)


class EmployeeSelfUpdateView(UpdateView):
    # template_name_suffix = '_form'
    model = Employee
    template_name = 'employee/employee_self_update_form.html'
    fields = [
        'last_name', 'first_name', 'middle_name',
        'tel_mobile', 'tel_other',
        'is_signer'
    ]
    success_url = '/'

    def get_object(self, queryset=None):
        return self.request.user

