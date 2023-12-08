from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from django.forms import ModelForm
from phonenumber_field.modelfields import PhoneNumberField
from .company import Company


class Employee(AbstractUser):

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    company = models.ForeignKey(to=Company, related_name='employees', null=True, on_delete=models.CASCADE)
    available_companies = models.ManyToManyField(Company, related_name="managing_users", db_table='employee_companies')
    middle_name = models.CharField(_('middle name'), max_length=150, blank=True)
    email = models.EmailField(
        _('email address'),
        blank=False,
        unique=True,
        error_messages={
            'unique': _("Current e-mail cannot be registered"),
        }
    )
    tel_mobile = PhoneNumberField(blank=False)
    tel_other = PhoneNumberField(blank=True)
    is_signer = models.BooleanField(_('Granted to sign documents'), default=False)

    class Meta:
        db_table = 'employees'
        ordering = ['-is_signer']

    def __str__(self):
        return f'{self.name_short()}'

    def name_full(self):
        return "{} {} {}".format(self.last_name, self.first_name, self.middle_name)

    def name_short(self):
        return "{} {}. {}.".format(self.last_name, self.first_name[:1], self.middle_name[:1])


class EmployeeSelfUpdateForm(ModelForm):
    class Meta:
        model = Employee
        fields = [
            'last_name', 'first_name', 'middle_name',
            'tel_mobile', 'tel_other',
            'is_signer'
        ]
