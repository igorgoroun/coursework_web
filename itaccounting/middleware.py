from django.conf import settings
from django.utils import translation


class ForceLangMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization

    def __call__(self, request):
        request.LANG = getattr(settings, 'LANGUAGE_CODE', settings.LANGUAGE_CODE)
        translation.activate(request.LANG)
        request.LANGUAGE_CODE = request.LANG
        response = self.get_response(request)
        return response