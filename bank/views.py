from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpRequest, HttpResponseRedirect
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from bank.models import BankAccount
from company.models.partner import Partner

import logging
_logger = logging.getLogger(__name__)


class CompanyBankAccountCreateView(LoginRequiredMixin, CreateView):
    model = BankAccount
    template_name = 'bank_account_company_form.html'
    success_url = reverse_lazy('setup_dashboard')
    fields = [
        'iban',
        'bank_name',
        'currency',
        'actual'
    ]

    def form_valid(self, form):
        form.instance.company = self.request.user.company
        return super().form_valid(form)


class CompanyBankAccountUpdateView(LoginRequiredMixin, UpdateView):
    model = BankAccount
    template_name = 'bank_account_company_form.html'
    success_url = reverse_lazy('setup_dashboard')
    fields = [
        'iban',
        'bank_name',
        'currency',
        'actual'
    ]


class PartnerBankAccountCreateView(LoginRequiredMixin, CreateView):
    model = BankAccount
    template_name = 'bank_account_company_form.html'
    fields = [
        'iban',
        'bank_name',
        'currency',
        'actual'
    ]

    def get_success_url(self):
        return reverse_lazy('partner_details', kwargs={'pk': self.kwargs.get('partner_id')})

    def form_valid(self, form):
        form.instance.partner = Partner.objects.get(pk=self.kwargs.get('partner_id'))
        form.instance.company = self.request.user.company
        return super(PartnerBankAccountCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['partner'] = Partner.objects.get(pk=self.kwargs.get('partner_id'))
        return context


class PartnerBankAccountUpdateView(LoginRequiredMixin, UpdateView):
    model = BankAccount
    template_name = 'bank_account_company_form.html'
    fields = [
        'iban',
        'bank_name',
        'currency',
        'actual'
    ]

    def get_success_url(self):
        return reverse_lazy('partner_details', kwargs={'pk': self.object.partner.pk})
