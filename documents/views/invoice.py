from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.http import HttpRequest, HttpResponseRedirect
from django.views import View
from num2words import num2words
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from documents.models.invoice import Invoice, InvoiceLine, InvoiceFormForPartner, InvoiceLineFormSet, InvoiceFormForContract
from documents.models.contract import Contract
from documents.models.sequence import Sequence
from company.models.partner import Partner
from company.models.company import Company
from company.models.employee import Employee
from company.models.representative import Representative

import logging

_logger = logging.getLogger(__name__)


class InvoiceListView(LoginRequiredMixin, ListView):
    template_name = 'invoice/list.html'
    context_object_name = 'invoices'
    model = Invoice

    def get_queryset(self):
        return Invoice.objects.filter(company=self.request.user.company.id).order_by('-issue_date', '-number')


class InvoicePrintView(LoginRequiredMixin, DetailView):
    template_name = 'invoice/print_ua.html'
    context_object_name = 'invoice'
    model = Invoice

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        invoice = context.get('object')
        context['amount_string'] = num2words(invoice.amount, lang='uk', to='currency', currency='UAH')
        _logger.info(f"Foreign: {invoice.partner.is_foreign}")
        if invoice.partner.is_foreign:
            self.template_name = 'invoice/print_foreign.html'
        if invoice.type == 'customer_invoice':
            context['vendor'] = invoice.company
            context['customer'] = invoice.partner
        return context


class InvoiceUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'invoice/form.html'
    model = Invoice
    fields = [
        'reference',
        # 'partner',
        'issue_date',
        'currency',
        'origin_contract',
    ]

    #def get_context_data(self, **kwargs):
    #    context = super().get_context_data(**kwargs)
    #    context["partner"] = Partner.objects.get(pk=self.kwargs.get('partner_id'))
    #    return context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        _logger.warning(context)
        invoice = context.get('object')
        context["partner"] = invoice.partner
        context["invoice_lines_formset"] = InvoiceLineFormSet(instance=invoice)
        return context

    def get_success_url(self):
        # return reverse_lazy('partner_details', kwargs={'pk': self.kwargs.get('partner_id')})
        return reverse_lazy('invoice_list', kwargs={})


class InvoiceRemoveView(LoginRequiredMixin, DeleteView):
    model = Invoice
    success_url = reverse_lazy('invoice_list')
    template_name = "confirm_delete.html"


class InvoiceCreateForPartnerFormView(LoginRequiredMixin, FormView):
    template_name = 'invoice/form.html'
    form_class = InvoiceFormForPartner
    success_url = reverse_lazy('invoice_list')

    def get_initial(self):
        _logger.info("Enter get_initial")
        initial = super().get_initial()
        try:
            company = self.request.user.company
            assert type(company) == Company
            initial.update({
                'partner': Partner.objects.get(pk=self.kwargs.get('partner_id')),
                'company': company,
                'company_signer': company.employees.first()
            })
        except:
            pass
        _logger.info(f"Initials from partner: {initial}")
        return initial

    def get_context_data(self, **kwargs):
        _logger.info(f"Enter get_context_data: {kwargs}")
        context = super().get_context_data(**kwargs)
        try:
            context["partner"] = Partner.objects.get(pk=self.kwargs.get('partner_id'))
        except:
            pass
        context["company"] = self.request.user.company
        context["invoice_lines_formset"] = InvoiceLineFormSet()
        _logger.info(f"Exiting context: {context}")
        return context

    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def post(self, request, *args, **kwargs):
        _logger.info(f"Entering post: {request}, {args}, {kwargs}")
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        lines_formset = InvoiceLineFormSet(self.request.POST)
        if not form.is_valid():
            _logger.warning("Invoice form invalid")
            return self.form_invalid(form)
        if not lines_formset.is_valid():
            _logger.warning("Invoice lines form invalid")
            return self.form_invalid(lines_formset)
        return self.form_valid(form, lines_formset)

    def form_valid(self, form, lines_formset):
        form.instance.created_by = self.request.user
        invoice_seq = Sequence(company=self.request.user.company, document='invoice',
                               document_date=form.instance.issue_date)
        form.instance.number = next(invoice_seq).get('string')
        form.instance.company = self.request.user.company
        _logger.info(f"Form instance lines: {form.instance.lines}")
        self.object = form.save(commit=False)
        self.object.save()
        # saving Instances
        lines = lines_formset.save(commit=False)
        for meta in lines:
            meta.invoice = self.object
            meta.save()
        return super(InvoiceCreateForPartnerFormView, self).form_valid(form)


class InvoiceCreateForContractFormView(InvoiceCreateForPartnerFormView):
    form_class = InvoiceFormForContract

    def get_initial(self):
        _logger.info("Enter get_initial from contract")
        context = super().get_initial()
        try:
            origin_contract = Contract.objects.get(pk=self.kwargs.get('contract_id'))
            context['origin_contract'] = origin_contract
            context['currency'] = origin_contract.currency
            context["partner"] = origin_contract.partner
            context["partner_signer"] = origin_contract.partner_signer
            context["company"] = origin_contract.company
            context["company_signer"] = origin_contract.company_signer
        except:
            pass
        _logger.info(f"Initials from contract: {context}")
        return context

    def get_context_data(self, **kwargs):
        _logger.info(f"Enter get_context_data: {kwargs}")
        context = super().get_context_data(**kwargs)
        origin_contract = Contract.objects.get(pk=self.kwargs.get('contract_id'))
        context['origin_contract'] = origin_contract
        context['currency'] = origin_contract.currency
        context["partner"] = origin_contract.partner
        context["partner_signer"] = origin_contract.partner_signer
        context["company"] = origin_contract.company
        context["company_signer"] = origin_contract.company_signer
        context["invoice_lines_formset"] = InvoiceLineFormSet()
        _logger.info(f"Exiting context: {context}")
        return context
