from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.http import HttpRequest, HttpResponseRedirect
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from documents.models.contract import Contract
from company.models.partner import Partner
from company.models.company import Company
from company.models.employee import Employee
from company.models.representative import Representative
from documents.models.sequence import SequenceSetup

import logging

_logger = logging.getLogger(__name__)


class IsMyCompanySequenceMixin(UserPassesTestMixin):
    def test_func(self):
        # partner_id = self.kwargs.get('partner_id', None)
        return True     # partner_id == self.request.user.company


class SequenceListView(LoginRequiredMixin, ListView):
    template_name = 'sequence/list.html'
    context_object_name = 'sequences'
    model = SequenceSetup

    def get_queryset(self):
        return SequenceSetup.objects.filter(company=self.request.user.company.pk)


class SequenceUpdateView(LoginRequiredMixin, IsMyCompanySequenceMixin, UpdateView):
    template_name = 'sequence/form.html'
    success_url = reverse_lazy('sequence_list')
    model = SequenceSetup
    fields = [
        'document',
        'mask',
        'step',
    ]


class SequenceCreateView(LoginRequiredMixin, CreateView):
    template_name = 'sequence/form.html'
    success_url = reverse_lazy('sequence_list')
    model = SequenceSetup
    fields = [
        'document',
        'mask',
        'step',
    ]

    def form_valid(self, form):
        form.instance.company = self.request.user.company
        return super(SequenceCreateView, self).form_valid(form)


