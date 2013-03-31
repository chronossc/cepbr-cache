from __future__ import absolute_import

from django.conf.urls import patterns, url

from .views import get_cep


urlpatterns = patterns(
    '',
    url(r'^cepbrcache/get_cep/$', get_cep, name='get_cep'),
)
