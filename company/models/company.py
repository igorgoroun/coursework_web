from django.db import models
from django.forms import ModelForm
from django.utils.translation import gettext as _
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework import serializers
import logging

_logger = logging.getLogger(__name__)


# Company model
class Company(models.Model):
    code_short = _('FOP')
    code_full = _('Entrepreneur')

    name_last = models.CharField(verbose_name=_('Last name'), blank=False, max_length=64)
    name_first = models.CharField(verbose_name=_('First name'), blank=False, max_length=64)
    name_middle = models.CharField(verbose_name=_('Middle name'), blank=False, max_length=64)
    address_line_1 = models.CharField(verbose_name=_('Address line 1'), max_length=128)
    address_line_2 = models.CharField(verbose_name=_('Address line 2'), max_length=128)
    address_line_3 = models.CharField(verbose_name=_('Address line 3'), blank=True, max_length=128)
    tel_number = PhoneNumberField(blank=True)
    tel_fax = PhoneNumberField(blank=True)
    itn = models.CharField(verbose_name=_('Personal tax number'), max_length=16)
    reg = models.CharField(verbose_name=_('Legacy registration number'), max_length=32)

    class Meta:
        db_table = 'companies'

    def __str__(self):
        return f'{self.fop_name_short()}'

    def __setattr__(self, key, value):
        if key in ['name_last', 'name_first', 'name_middle']:
            value = str(value).capitalize()
        super().__setattr__(key, value)

    def main_bank_account(self):
        _logger.warning(f"FUCKING ACCOUNT: {self.bank_accounts.filter(actual=True, company=self.id, partner=None).first()}")
        return self.bank_accounts.filter(actual=True, company=self.id, partner=None).first()

    def fop_name_full(self):
        return "{} {} {} {}".format(self.code_full, self.name_last, self.name_first, self.name_middle)

    def fop_name_short(self):
        return "{} {} {}. {}.".format(self.code_short, self.name_last, self.name_first[:1], self.name_middle[:1])

    def own_name_full(self):
        return "{} {} {}".format(self.name_last, self.name_first, self.name_middle)

    def own_name_short(self):
        return "{} {}. {}.".format(self.name_last, self.name_first[:1], self.name_middle[:1])

    def address(self):
        return "{} {} {}".format(self.address_line_1, self.address_line_2, self.address_line_3)


class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = [
            'name_last', 'name_first', 'name_middle',
            'address_line_1', 'address_line_2', 'address_line_3',
            'tel_number', 'tel_fax',
            'itn', 'reg'
        ]


# Company Serializer
class CompanySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'name_last', 'name_first', 'name_middle')
