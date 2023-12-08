from django.shortcuts import render
from django.http import HttpRequest
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


class HomepageView(LoginRequiredMixin, View):

    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        """
        :param request
        :type request HttpRequest
        """
        return render(request, 'homepage.html', {'user': request.user})


class SetupDashboardView(LoginRequiredMixin, View):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        """
        :param request
        :type request HttpRequest
        """

        personal_accounts = request.user.company.bank_accounts.filter(partner=None)

        return render(request, 'setup.html', context={'bank_accounts': personal_accounts})
