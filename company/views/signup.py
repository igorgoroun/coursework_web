from django.shortcuts import render
from django.http import HttpRequest
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


class SignupView(View):

    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        """
        :param request
        :type request HttpRequest
        """
        return render(request, 'homepage.html', {'user': request.user})