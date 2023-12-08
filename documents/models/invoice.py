from django.db import models
from django.forms import ModelForm, BaseInlineFormSet, inlineformset_factory
from django import forms
from django.utils.translation import gettext as _
from django.utils.functional import cached_property
from django.utils import timezone
from company.models import Employee, Company, Partner, Representative
from documents.models import Contract
from bank.models import CURRENCIES, DEFAULT_CURRENCY

import logging

_logger = logging.getLogger(__name__)


class Invoice(models.Model):

    type = models.CharField(verbose_name=_('Invoice direction'), blank=False, choices=[
        ('customer_invoice', 'Issued by me for customer'),
        ('vendor_bill', 'Received from vendor')
    ], default='customer_invoice', max_length=16, )
    number = models.CharField(verbose_name=_('Invoice number'), blank=False, max_length=128, )
    reference = models.CharField(verbose_name=_('External reference'), blank=True, max_length=128, )
    company = models.ForeignKey(to=Company, blank=False, on_delete=models.DO_NOTHING, verbose_name=_('Issuer company'), )
    company_signer = models.ForeignKey(to=Employee, blank=False, related_name='signed_invoices', on_delete=models.DO_NOTHING, verbose_name=_('Signer from my side'), )
    partner = models.ForeignKey(to=Partner, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name=_('Customer'), )
    issue_date = models.DateField(verbose_name=_('Issue date'), default=timezone.now, )
    created_by = models.ForeignKey(to=Employee, on_delete=models.DO_NOTHING, related_name='created_invoices', verbose_name=_('Created by user'), )
    origin_contract = models.ForeignKey(to=Contract, on_delete=models.DO_NOTHING, blank=True, null=True, related_name="invoices", verbose_name=_('Origin Contract'), )
    currency = models.CharField(verbose_name=_('Currency'), max_length=3, default=DEFAULT_CURRENCY, choices=CURRENCIES, null=False, blank=False, )
    notes = models.TextField(verbose_name=_('Com short notes'), blank=True, )

    class Meta:
        db_table = 'invoices'
        ordering = ['-issue_date']

    def __str__(self):
        return self.reference or self.number or self.pk

    @property
    def amount(self):
        # return sum(self.lines.all().aggregate(models.Sum('amount')))
        return sum([line.amount for line in self.lines.all()])


class InvoiceLine(models.Model):

    invoice = models.ForeignKey(to=Invoice, on_delete=models.CASCADE, related_name='lines', verbose_name=_('Invoice'), )
    product_hint = models.CharField(verbose_name=_('Product description'), blank=False, max_length=255, )
    # product_uom = models.ForeignKey()
    product_uom_hint = models.CharField(verbose_name=_('UOM hint'), max_length=16, blank=False, )
    qty = models.FloatField(verbose_name=_('Product quantity'), blank=False, null=False, )
    price = models.FloatField(verbose_name=_('Unit price'), blank=False, )

    class Meta:
        db_table = 'invoice_lines'

    def __str__(self):
        return f"{self.qty}{self.product_uom_hint} * {self.product_hint}: {self.amount}"

    @cached_property
    def amount(self):
        return round(self.qty * self.price, 2)


class InvoiceFormForPartner(ModelForm):
    class Meta:
        model = Invoice
        fields = ['reference', 'company', 'company_signer', 'partner', 'currency']


class InvoiceFormForContract(ModelForm):
    class Meta:
        model = Invoice
        fields = ['reference', 'company', 'company_signer', 'partner', 'currency']


class InvoiceLineForm(ModelForm):
    class Meta:
        model = InvoiceLine
        fields = ('product_hint', 'product_uom_hint', 'qty', 'price')


InvoiceLineFormSet = inlineformset_factory(Invoice, InvoiceLine, form=InvoiceLineForm, extra=3, )

