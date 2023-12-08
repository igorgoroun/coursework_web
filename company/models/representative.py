from django.db import models
from django.utils.translation import gettext as _
from phonenumber_field.modelfields import PhoneNumberField
from .partner import Partner


class Representative(models.Model):
    partner = models.ForeignKey(to=Partner, related_name='representatives', null=True, on_delete=models.SET_NULL, )
    last_name = models.CharField(max_length=64, blank=True)
    first_name = models.CharField(max_length=64, blank=True)
    middle_name = models.CharField(max_length=64, blank=True)
    position = models.CharField(max_length=16, blank=True)
    email = models.EmailField(
        _('Email address'),
        blank=True,
        null=True,
        unique=True,
        error_messages={
            'unique': _("Current e-mail cannot be registered"),
        }
    )
    tel_mobile = PhoneNumberField(blank=True)
    tel_number = PhoneNumberField(blank=True)
    notes = models.TextField(null=True, blank=True)
    is_signer = models.BooleanField(_('Granted to sign documents'), default=False)

    class Meta:
        db_table = 'partners_represenatives'
        unique_together = ['partner', 'is_signer']

    def __str__(self):
        return self.name_short()

    def __setattr__(self, key, value):
        if key in ['last_name', 'first_name', 'middle_name']:
            value = str(value).capitalize()
        super().__setattr__(key, value)

    def name_full(self):
        return "{} {} {}".format(self.last_name, self.first_name, self.middle_name)

    def name_short(self):
        return "{} {}. {}.".format(self.last_name, self.first_name[:1], self.middle_name[:1])


