# coding: utf-8

import cepbrcache

from django.conf import settings
from django.http import HttpResponse


def get_cep(request):
    if request.is_ajax() or settings.DEBUG:
        value = request.GET.get('zip', None)
        cep = cepbrcache.get_cep(value)
        return HttpResponse(
            cep.json(),
            content_type="application/json")
    return HttpResponse('Indisponivel')