from django.db import models
from django.utils.translation import gettext as _
from django.utils import timezone
from bank.models import DEFAULT_CURRENCY, CURRENCIES
from company.models import Employee, Company, Partner, Representative
from datetime import date


class Contract(models.Model):

    number = models.CharField(verbose_name=_('Contract number'), blank=False, max_length=128, )  # type: ignore[var-annotated]
    reference = models.CharField(verbose_name=_('External reference'), blank=True, max_length=128, )  # type: ignore[var-annotated]
    company = models.ForeignKey(to=Company, blank=False, on_delete=models.DO_NOTHING, verbose_name=_('My side'), )  # type: ignore[var-annotated]
    company_signer = models.ForeignKey(to=Employee, blank=False, related_name='signed_contracts', on_delete=models.DO_NOTHING, verbose_name=_('Signer from my side'), )  # type: ignore[var-annotated]
    partner = models.ForeignKey(to=Partner, blank=False, on_delete=models.DO_NOTHING, verbose_name=_('Partner side'), )
    partner_signer = models.ForeignKey(to=Representative, blank=False, on_delete=models.DO_NOTHING, verbose_name=_('Signer from partner side'), )
    sign_date = models.DateField(verbose_name=_('Sign date'), default=timezone.now, )
    closing_date = models.DateField(verbose_name=_('Contract closing date'), blank=True, default=date(date.today().year, 12, 31), )
    unlimited = models.BooleanField(verbose_name=_('Contract has infinite validity'), )
    created_by = models.ForeignKey(to=Employee, on_delete=models.DO_NOTHING, related_name='created_contracts', verbose_name=_('Created by user'), )
    currency = models.CharField(verbose_name=_('Currency'), max_length=3, default=DEFAULT_CURRENCY, choices=CURRENCIES, null=False, blank=False, )
    price = models.FloatField(verbose_name=_('Total price'), default=0.0, null=True, blank=True, )
    notes = models.TextField(verbose_name=_('Contract short notes'), blank=True, )

    class Meta:
        db_table = 'contracts'

    def __str__(self):
        return f"{self.reference or self.number or self.pk} ({self.partner}) {self.sign_date}"

    @property
    def amount(self):
        return self.price + sum([ext.price for ext in self.extensions.all()]) or 0.0


class ContractExtension(models.Model):
    contract = models.ForeignKey(to=Contract, verbose_name=_('Contract'), related_name='extensions', on_delete=models.CASCADE, blank=False, )  # type: ignore[var-annotated]
    reference = models.CharField(verbose_name=_('Reference'), null=False, blank=False, max_length=128, )  # type: ignore[var-annotated]
    sign_date = models.DateField(verbose_name=_('Sign date'), default=timezone.now, )
    price = models.FloatField(verbose_name=_('Price'), default=0.0, null=False, blank=False, )
    notes = models.TextField(verbose_name=_('Short notes'), blank=True, )
