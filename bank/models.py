from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.forms import ModelForm
from django.utils.translation import gettext as _
from company.models import Company, Partner
from rest_framework import serializers
import re
import logging

_logger = logging.getLogger(__name__)


DEFAULT_CURRENCY = "UAH"
CURRENCIES = [
    (DEFAULT_CURRENCY, _(DEFAULT_CURRENCY)),
    ("EUR", "Euro"),
    ("USD", "US Dollar"),
    ("CHF", "CHF")
]
TRDEF = _("UAH")


class BankAccount(models.Model):
    class Meta:
        ordering = ['-actual', '-id']

    iban_max_length = 64

    account_number = models.CharField(max_length=32, default=None, null=True)  # type: ignore[var-annotated]
    iban = models.CharField(max_length=iban_max_length, default=None, null=False)  # type: ignore
    bank_number = models.CharField(max_length=6, default=None, blank=True, null=True)  # type: ignore
    bank_name = models.CharField(max_length=64, default=None, blank=True, null=True)  # type: ignore
    actual = models.BooleanField(verbose_name=_('Actual account'), default=False, )
    company = models.ForeignKey(
        to=Company,
        related_name="bank_accounts",
        null=True,
        on_delete=models.SET_NULL,
    )  # type: ignore
    partner = models.ForeignKey(
        to=Partner,
        related_name="bank_accounts",
        null=True,
        on_delete=models.SET_NULL,
    )  # type: ignore
    currency = models.CharField(
        max_length=3,
        default=DEFAULT_CURRENCY,
        choices=CURRENCIES,
        null=False,
        blank=False,
    )  # type: ignore

    def __str__(self):
        return f"{self.iban_readable()} ({self.currency})"

    def __setattr__(self, key, value):
        if key in ["iban"]:
            value = str(value).replace(" ", "").upper()
            value = value[:29] if len(value) > 29 else value
        super().__setattr__(key, value)

    def iban_readable(self):
        # UA03 326610 00000 26006555262001
        return "{} {} {} {}".format(
            self.iban[0:4], self.iban[4:10], self.iban[10:15], self.iban[15:]
        )


@receiver(pre_save, sender=BankAccount)
def format_bank_account(sender, **kwargs):
    acc = kwargs.get("instance", None)
    if type(acc) == BankAccount:
        # replace spaces and special symbols
        acc.iban = re.sub(r"[\s_-]+", "", acc.iban)
        acc.account_number = acc.iban[15:]
        _logger.debug(f"PRE-SAVE actual is: {acc.actual}")
        # check actual
        if acc.actual is True:
            other_accounts = BankAccount.objects.filter(partner=acc.partner, company=acc.company).exclude(pk=acc.pk)
            _logger.debug(f"Found other accounts: {other_accounts}")
            other_accounts.update(actual=False)


class BankAccountForCompanyForm(ModelForm):
    class Meta:
        model = BankAccount
        fields = ["currency", "iban", "bank_number", "bank_name"]


class BankAccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BankAccount
        fields = ("id", "iban", "bank_name", "company", "partner")
