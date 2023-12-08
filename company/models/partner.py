from django.db import models
from django.utils.translation import gettext as _
from phonenumber_field.modelfields import PhoneNumberField
from .company import Company


class Partner(models.Model):
    company = models.ForeignKey(to=Company, related_name='partners', null=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    address_line_1 = models.CharField(max_length=128, blank=True)
    address_line_2 = models.CharField(max_length=128, blank=True)
    address_line_3 = models.CharField(max_length=128, blank=True)
    tel_number = PhoneNumberField(blank=True)
    tel_fax = PhoneNumberField(blank=True)
    itn = models.CharField(max_length=16, blank=True)
    reg = models.CharField(max_length=32, blank=True)
    notes = models.TextField(null=True, blank=True)
    is_foreign = models.BooleanField(default=False, )

    class Meta:
        db_table = 'partners'

    def __str__(self):
        return self.name

    def __setattr__(self, key, value):
        if key in ['representative_name_last', 'representative_name_first', 'representative_name_middle']:
            value = str(value).capitalize()
        super().__setattr__(key, value)

    def address(self):
        return "{} {} {}".format(self.address_line_1, self.address_line_2, self.address_line_3)

    @property
    def representative_main(self):
        person = self.representatives.filter(is_signer=True).first()
        return person

    def representative_name_full(self):
        return "{} {} {}".format(self.representative_main.last_name, self.representative_main.first_name, self.representative_main.middle_name)

    def representative_name_short(self):
        return "{} {}. {}.".format(self.representative_main.last_name, self.representative_main.first_name[:1], self.representative_main.middle_name[:1])
