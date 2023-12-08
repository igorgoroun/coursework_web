from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.http import HttpRequest, HttpResponseRedirect
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from company.models import Partner, Representative

import logging

_logger = logging.getLogger(__name__)


class IsMyRepresentativeMixin(UserPassesTestMixin):
    def test_func(self):
        partner_id = self.kwargs.get('partner_id', None)
        return partner_id == self.request.user.company


class PartnerRepresentativeListView(LoginRequiredMixin, ListView):
    template_name = 'partner/partner_list.html'
    context_object_name = 'representatives'
    model = Representative

    def get_queryset(self):
        return Partner.objects.filter(company=self.request.user.company.id)


class PartnerRepresentativeUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'partner/partner_representative_form.html'
    model = Representative
    fields = [
        'last_name',
        'first_name',
        'middle_name',
        'position',
        'is_signer',
        'email',
        'tel_mobile',
        'tel_number',
        'notes',
    ]

    def get_success_url(self):
        return reverse_lazy('partner_details', kwargs={'pk': self.kwargs.get('partner_id')})


class PartnerRepresentativeCreateView(LoginRequiredMixin, CreateView):
    template_name = 'partner/partner_representative_form.html'
    model = Representative
    fields = [
        'last_name',
        'first_name',
        'middle_name',
        'position',
        'is_signer',
        'email',
        'tel_mobile',
        'tel_number',
        'notes',
    ]

    def get_success_url(self):
        return reverse_lazy('partner_details', kwargs={'pk': self.kwargs.get('partner_id')})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["partner"] = Partner.objects.get(pk=self.kwargs.get('partner_id'))
        return context

    def form_valid(self, form):
        form.instance.partner = Partner.objects.get(pk=self.kwargs.get('partner_id'))
        return super(PartnerRepresentativeCreateView, self).form_valid(form)


