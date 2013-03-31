# coding: utf-8

from __future__ import absolute_import

import cepbrcache

from django.forms import Field
from django.core import validators
from django.core.exceptions import ValidationError

from .widgets import CepCacheWidget


class CepCacheField(Field):
    widget = CepCacheWidget

    def __init__(self, **kwargs):
        kwargs['label'] = ''
        super(CepCacheField, self).__init__(**kwargs)

    def to_python(self, value):
        if value in validators.EMPTY_VALUES:
            return None

        cep = value[0]

        try:
            value = cepbrcache.get_cep(cep)
        except Exception as e:
            raise ValidationError(e)
        return value
