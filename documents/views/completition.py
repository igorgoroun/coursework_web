from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.http import HttpRequest, HttpResponseRedirect
from django.views import View
from num2words import num2words
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from documents.models.contract import Contract
from documents.models.invoice import Invoice
from documents.models.completition import Completition, CompletitionLine, CompletitionFormForContract, CompletitionFormForInvoice, CompletitionLineFormSet
from documents.models.sequence import Sequence
from django.db.models import F, Aggregate, Sum, Count
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


class CompletitionListView(LoginRequiredMixin, ListView):
    template_name = 'completition/list.html'
    context_object_name = 'completitions'
    # readonly_fields = ['amount']
    model = Completition

    def get_queryset(self):
        return Completition.\
            objects.\
            filter(company=self.request.user.company.id).\
            order_by('-sign_date', '-number')
        # annotate(amount=Sum('lines__price'))


class CompletitionPrintView(LoginRequiredMixin, DetailView):
    template_name = 'completition/print_ua.html'
    context_object_name = 'completition'
    model = Completition

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        completition = context.get('object')
        context['amount_string'] = num2words(completition.amount, lang='uk', to='currency', currency='UAH')
        return context


class CompletitionUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'completition/form.html'
    model = Completition
    fields = [
        'reference',
        'partner',
        'partner_signer',
        'sign_date',
        # 'closing_date',
        'origin_contract'
    ]

    # def get_context_data(self, **kwargs):
    #    context = super().get_context_data(**kwargs)
    #    context["partner"] = Partner.objects.get(pk=self.kwargs.get('partner_id'))
    #    return context

    def get_success_url(self):
        # return reverse_lazy('partner_details', kwargs={'pk': self.kwargs.get('partner_id')})
        return reverse_lazy('completition_list', kwargs={})


class CompletitionCreateForPartnerView(LoginRequiredMixin, CreateView):
    template_name = 'completition/form.html'
    model = Completition
    success_url = reverse_lazy('completition_list')
    fields = [
        'reference',
        'partner_signer',
        'sign_date',
        'origin_contract',
        'currency'
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
        seq = Sequence(company=self.request.user.company, document='completition', document_date=form.instance.sign_date)
        form.instance.number = next(seq).get('string')
        partner_signer = Representative.objects.filter(is_signer=True, partner=form.instance.partner).first()
        form.instance.partner_signer = partner_signer
        company_signer = Employee.objects.filter(is_signer=True, company=form.instance.company).first()
        form.instance.company_signer = company_signer
        return super().form_valid(form)


class CompletitionCreateForContractView(LoginRequiredMixin, CreateView):
    form_class = CompletitionFormForContract
    template_name = 'completition/form.html'
    # model = Completition
    success_url = reverse_lazy('completition_list')
    # fields = [
    #     'reference',
    #     'origin_contract',
    #     'partner',
    #     'partner_signer',
    #     'sign_date',
    #     'currency'
    # ]

    def get_initial(self):
        _logger.info("Enter get_initial")
        initial = super().get_initial()
        try:
            origin_contract = Contract.objects.get(pk=self.kwargs.get('contract_id'))
            initial.update({
                'origin_contract': origin_contract,
                'partner': origin_contract.partner,
                'partner_signer': origin_contract.partner_signer,
                'company': origin_contract.company,
                'company_signer': origin_contract.company_signer,
            })
        except:
            pass
        _logger.info(f"Initials from contract: {initial}")
        return initial

    def get_context_data(self, **kwargs):
        _logger.info(f"Enter get_context_data: {kwargs}")
        context = super().get_context_data(**kwargs)
        context["company"] = self.request.user.company
        context["completition_lines_formset"] = CompletitionLineFormSet()
        _logger.info(f"Exiting context: {context}")
        return context

    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def post(self, request, *args, **kwargs):
        _logger.info(f"Entering completition post: {request}, {args}, {kwargs}")
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        lines_formset = CompletitionLineFormSet(self.request.POST)
        if not form.is_valid():
            _logger.warning("Completition form invalid")
            return self.form_invalid(form)
        if not lines_formset.is_valid():
            _logger.warning("Completition lines form invalid")
            return self.form_invalid(lines_formset)
        return self.form_valid(form, lines_formset)

    def form_valid(self, form, lines_formset):
        form.instance.created_by = self.request.user
        invoice_seq = Sequence(company=self.request.user.company, document='completition',
                               document_date=form.instance.sign_date)
        form.instance.number = next(invoice_seq).get('string')
        form.instance.company = self.request.user.company
        self.object = form.save(commit=False)
        self.object.save()
        # saving Instances
        lines = lines_formset.save(commit=False)
        for meta in lines:
            meta.completition = self.object
            meta.save()
        return super().form_valid(form)


class CompletitionCreateForInvoiceView(CompletitionCreateForContractView):
    form_class = CompletitionFormForInvoice

    def get_initial(self):
        _logger.info("Enter get_initial completition for invoice")
        initial = super().get_initial()
        origin_invoice = Invoice.objects.get(pk=self.kwargs.get('invoice_id'))
        # update completition
        initial.update({
            'origin_invoice': origin_invoice,
            'partner': origin_invoice.partner,
            'partner_signer': origin_invoice.partner.representative_main,
            'company': origin_invoice.company,
            'company_signer': origin_invoice.company_signer,
        })
        _logger.info(f"Initials from completition for invoice: {initial}")
        return initial

    def get_context_data(self, **kwargs):
        _logger.info(f"Enter get_context_data FROM INVOICE: {kwargs}")
        context = super().get_context_data(**kwargs)
        origin_invoice = Invoice.objects.get(pk=self.kwargs.get('invoice_id'))
        # checking invoice lines
        lines = []
        for il in origin_invoice.lines.all():
            lines.append({'product_hint': il.product_hint, 'product_uom_hint': il.product_uom_hint, 'qty': il.qty, 'price': il.price})
        context["completition_lines_formset"] = CompletitionLineFormSet(initial=lines)
        return context
