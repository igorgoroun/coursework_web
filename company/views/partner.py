from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.http import HttpRequest, HttpResponseRedirect
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from company.models import Partner

import logging

_logger = logging.getLogger(__name__)


class IsMyPartnerMixin(UserPassesTestMixin):
    def test_func(self):
        partner = self.get_object()
        return partner.company == self.request.user.company


class PartnerDetailsView(LoginRequiredMixin, IsMyPartnerMixin, DetailView):
    template_name = 'partner/partner_details.html'
    context_object_name = 'partner'
    model = Partner


class PartnerListView(LoginRequiredMixin, ListView):
    template_name = 'partner/partner_list.html'
    context_object_name = 'partners'
    model = Partner

    def get_queryset(self):
        return Partner.objects.filter(company=self.request.user.company.id)


class PartnerUpdateView(LoginRequiredMixin, IsMyPartnerMixin, UpdateView):
    template_name = 'partner/partner_form.html'
    model = Partner
    fields = [
        'name',
        'address_line_1',
        'address_line_2',
        'address_line_3',
        'tel_number',
        'tel_fax',
        'itn',
        'notes',
        'is_foreign',
    ]
    success_url = reverse_lazy('partner_list')


class PartnerCreateView(LoginRequiredMixin, CreateView):
    template_name = 'partner/partner_form.html'
    model = Partner
    fields = [
        'name',
        'address_line_1',
        'address_line_2',
        'address_line_3',
        'tel_number',
        'tel_fax',
        'itn',
        'notes',
        'is_foreign',
    ]
    success_url = reverse_lazy('partner_list')

    def form_valid(self, form):

        form.instance.company = self.request.user.company
        return super(PartnerCreateView, self).form_valid(form)


