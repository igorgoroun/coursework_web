from django.db import models
from django.utils.translation import gettext as _
from django.utils.functional import cached_property
from django.utils import timezone
from company.models import Employee, Company, Partner, Representative
from bank.models import CURRENCIES, DEFAULT_CURRENCY
from documents.models import Contract
from documents.models.invoice import Invoice
from django.forms import ModelForm, BaseInlineFormSet, inlineformset_factory
from datetime import date


class Completition(models.Model):

    number = models.CharField(verbose_name=_('Contract number'), blank=False, max_length=128, )
    reference = models.CharField(verbose_name=_('External reference'), blank=True, max_length=128, )
    company = models.ForeignKey(to=Company, blank=False, on_delete=models.DO_NOTHING, verbose_name=_('My side'), )
    company_signer = models.ForeignKey(to=Employee, blank=False, related_name='signed_completitions', on_delete=models.DO_NOTHING, verbose_name=_('Signer from my side'), )
    partner = models.ForeignKey(to=Partner, blank=False, on_delete=models.DO_NOTHING, verbose_name=_('Partner side'), )
    partner_signer = models.ForeignKey(to=Representative, blank=False, on_delete=models.DO_NOTHING, verbose_name=_('Signer from partner side'), )
    # limit_choices_to=models.Q('partner__pk' == partner) if partner else []
    sign_date = models.DateField(verbose_name=_('Sign date'), default=timezone.now, )
    created_by = models.ForeignKey(to=Employee, on_delete=models.DO_NOTHING, related_name='created_completitions', verbose_name=_('Created by user'), )
    # notes = models.TextField(verbose_name=_('Com short notes'), blank=True, )
    origin_contract = models.ForeignKey(to=Contract, on_delete=models.DO_NOTHING, blank=True, null=True, related_name="completitions", verbose_name=_('Origin Contract'), )
    origin_invoice = models.ForeignKey(to=Invoice, on_delete=models.DO_NOTHING, blank=True, null=True, related_name="completitions", verbose_name=_('Origin Invoice'), )
    currency = models.CharField(verbose_name=_('Currency'), choices=CURRENCIES, default=DEFAULT_CURRENCY, max_length=3, null=False, blank=False, )

    class Meta:
        db_table = 'completitions'

    def __str__(self):
        return self.reference or self.number or self.pk

    @property
    def amount(self):
        # return sum(self.lines.all().aggregate(models.Sum('amount')))
        return sum([line.amount for line in self.lines.all()])


class CompletitionLine(models.Model):

    completition = models.ForeignKey(to=Completition, on_delete=models.CASCADE, related_name='lines', verbose_name=_('Completition certificate'), )
    product_hint = models.CharField(verbose_name=_('Product description'), blank=False, max_length=255, )
    # product_uom = models.ForeignKey()
    product_uom_hint = models.CharField(verbose_name=_('UOM hint'), max_length=16, blank=False, )
    qty = models.FloatField(verbose_name=_('Product quantity'), blank=False, null=False, )
    price = models.FloatField(verbose_name=_('Unit price'), blank=False, )

    class Meta:
        db_table = 'completition_lines'

    def __str__(self):
        return f"{self.qty}{self.product_uom_hint} * {self.product_hint}: {self.amount}"

    @cached_property
    def amount(self):
        return round(self.qty * self.price, 2)


class CompletitionFormForContract(ModelForm):
    class Meta:
        model = Completition
        fields = [
            'reference',
            'origin_contract',
            'partner',
            'partner_signer',
            # 'company',
            'company_signer',
            'sign_date',
            'currency'
        ]


class CompletitionFormForInvoice(ModelForm):
    class Meta:
        model = Completition
        fields = [
            'reference',
            'origin_invoice',
            'partner',
            'partner_signer',
            'company_signer',
            'sign_date',
            'currency'
        ]


class CompletitionLineForm(ModelForm):
    class Meta:
        model = CompletitionLine
        fields = ('product_hint', 'product_uom_hint', 'qty', 'price')


CompletitionLineFormSet = inlineformset_factory(Completition, CompletitionLine, form=CompletitionLineForm, extra=3, )

