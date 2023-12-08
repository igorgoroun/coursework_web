from abc import ABC
from django.db import models
from django.utils.translation import gettext as _
from django.utils.timezone import datetime
from django.template import Template, Context
from company.models import Company
from .contract import Contract
from .completition import Completition
from collections.abc import Generator
from datetime import date
import logging

_logger = logging.getLogger(__name__)


class Sequence(Generator):

    SEQUENCE_MAP = {
        'contract': Contract,
        'completition': Completition,
    }

    def __init__(self, company, document, document_date):
        """
        :param company              User's 'Company' object
        :type company Company
        :param document             Document sequence type
        :type document str
        :param document_date        Date to get sequence
        :type document_date date
        """
        super().__init__()
        s_types = list(zip(*SequenceSetup.SEQUENCE_TYPES))[0]
        if document not in s_types:
            raise ValueError(f'{_("Invalid document type")} {document}, {_("should be one of")} {s_types}')
        self.company = company
        self.document = document
        self.year = document_date.year
        self.month = document_date.month

    def send(self, ignored_vars=None) -> dict:
        """
        :returns: dict {
                'string': '2020/12/4512',
                'template': '{{ year }}/{{ month }}/{{ nr_month }}',
                'params': {'year': 2020, 'nr_year': 69541, 'month': 12, 'nr_month': 4512}
            }
        """
        _logger.info(f"Company {self.company.fop_name_short()} "
                     f"requested new {self.document} sequence number "
                     f"for year/month {self.year}/{self.month}")
        # find or create sequence setup
        seq_setup, setup_created = SequenceSetup.objects.get_or_create(company=self.company, document=self.document)
        # find an existed storage record for month and year
        storage = seq_setup.sequences.filter(year=self.year, month=self.month, company=self.company).first()
        if not storage:
            # let's try to find by year only
            storage = seq_setup.sequences.filter(year=self.year, company=self.company).order_by('-month').first()
            if not storage or storage.month > self.month:
                # create new seq storage for new both year and month
                storage = seq_setup.sequences.create(year=self.year, month=self.month, company=self.company)
            else:
                # create new seq storage for existed year and new month
                storage = seq_setup.sequences.create(year=self.year, month=self.month, company=self.company,
                                                     number_for_year=storage.number_for_year + 1)
        else:
            storage.number_for_year = 1 + storage.number_for_year
            storage.number_for_month = 1 + storage.number_for_month
            storage.save()
        tpl = Template(seq_setup.mask)
        params = {'year': storage.year, 'nr_year': storage.number_for_year, 'month': storage.month, 'nr_month': storage.number_for_month}
        return {
            'string': tpl.render(Context(params)),
            'template': seq_setup.mask,
            'params': params
        }

    def throw(self, type, value=None, traceback=None):
        _logger.error("Exception Thrown in Generator: I let go of the lock")
        #self.lock.release()
        raise StopIteration


class SequenceSetup(models.Model):

    SEQUENCE_TYPES = [
        ('invoice', _('Invoice')),
        ('completition', _('Completition certificate')),
        ('contract', _('Contract')),
        ('transaction', _('Bank transaction'))
    ]

    company = models.ForeignKey(to=Company, on_delete=models.CASCADE, blank=False, )
    document = models.CharField(verbose_name=_('Sequence type'), blank=False, null=False, choices=SEQUENCE_TYPES, max_length=32, )
    step = models.PositiveSmallIntegerField(verbose_name=_('Step'), default=1, )
    mask = models.CharField(verbose_name=_('Template in jinja format'), default="{{ year }}/{{ month }}/{{ nr_month }}", max_length=255, )

    class Meta:
        db_table = 'sequence_setup'
        constraints = [
            models.UniqueConstraint(fields=['company', 'document'], name='uniq_company_document'),
        ]


class SequenceStorage(models.Model):

    SEQUENCE_PARTS = [
        ('year', _('Year')),
        ('month', _('Month')),
        ('nr_year', _('Number for year')),
        ('nr_month', _('Number in document month')),
    ]
    setup = models.ForeignKey(to=SequenceSetup, related_name='sequences', on_delete=models.CASCADE, blank=False, )
    company = models.ForeignKey(to=Company, on_delete=models.CASCADE, blank=False, )
    year = models.PositiveSmallIntegerField(verbose_name=_('Year'), default=datetime.now().year, )
    number_for_year = models.IntegerField(verbose_name=_('Number in year'), blank=False, default=1, )
    month = models.PositiveSmallIntegerField(verbose_name=_('Month'), default=datetime.now().month, )
    number_for_month = models.IntegerField(verbose_name=_('Number in month'), blank=False, default=1, )

    class Meta:
        db_table = 'sequence_storage'
        constraints = [
            models.UniqueConstraint(fields=['setup', 'year', 'month'], name='uniq_setup_year_month')
        ]

    def __str__(self):
        return f"{self.year}:{self.number_for_year}/{self.month}:{self.number_for_month}"