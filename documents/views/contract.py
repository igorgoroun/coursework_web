from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.http import HttpRequest, HttpResponseRedirect
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from documents.models.contract import Contract
from documents.models.sequence import Sequence
from company.models.partner import Partner
from company.models.company import Company
from company.models.employee import Employee
from company.models.representative import Representative

import logging

_logger = logging.getLogger(__name__)


class IsMyCompanyContractMixin(UserPassesTestMixin):
    def test_func(self):
        # partner_id = self.kwargs.get('partner_id', None)
        return True     # partner_id == self.request.user.company


class ContractDetailView(LoginRequiredMixin, DetailView):
    template_name = 'contract/detail.html'
    model = Contract
    

class ContractListView(LoginRequiredMixin, ListView):
    template_name = 'contract/list.html'
    context_object_name = 'contracts'
    model = Contract

    def get_queryset(self):
        return Contract.objects.filter(company=self.request.user.company.id).order_by('-sign_date', '-number')


class ContractUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'contract/form.html'
    model = Contract
    fields = [
        'reference',
        'price',
        'currency',
        'partner',
        'partner_signer',
        'sign_date',
        'closing_date',
        'unlimited'
    ]

    #def get_context_data(self, **kwargs):
    #    context = super().get_context_data(**kwargs)
    #    context["partner"] = Partner.objects.get(pk=self.kwargs.get('partner_id'))
    #    return context

    def get_success_url(self):
        # return reverse_lazy('partner_details', kwargs={'pk': self.kwargs.get('partner_id')})
        return reverse_lazy('contract_list', kwargs={})


class ContractCreateForPartnerView(LoginRequiredMixin, CreateView):
    template_name = 'contract/form.html'
    model = Contract
    success_url = reverse_lazy('contract_list')
    fields = [
        'reference',
        'price',
        'currency',
        'sign_date',
        'closing_date',
        'unlimited'
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["partner"] = Partner.objects.get(pk=self.kwargs.get('partner_id'))
        context["company"] = self.request.user.company
        _logger.info(f"Context: {context}")
        return context

    def form_valid(self, form):
        form.instance.partner = Partner.objects.get(pk=self.kwargs.get('partner_id'))
        form.instance.company = self.request.user.company
        form.instance.created_by = self.request.user
        contract_seq = Sequence(company=self.request.user.company, document='contract', document_date=form.instance.sign_date)
        form.instance.number = next(contract_seq).get('string')
        partner_signer = Representative.objects.filter(is_signer=True, partner=form.instance.partner).first()
        form.instance.partner_signer = partner_signer
        company_signer = Employee.objects.filter(is_signer=True, company=form.instance.company).first()        
        form.instance.company_signer = company_signer
        return super(ContractCreateForPartnerView, self).form_valid(form)


