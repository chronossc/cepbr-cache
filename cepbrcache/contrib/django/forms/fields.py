# coding: utf-8

from __future__ import absolute_import

import cepbrcache

from django import forms
from django.core import validators
from django.core.exceptions import ValidationError


class CepCacheField(forms.Field):

    def to_python(self, value):
        if value in validators.EMPTY_VALUES:
            return None

        try:
            value = cepbrcache.get_cep(value)
        except ValueError as e:
            raise ValidationError(e)
        return value
