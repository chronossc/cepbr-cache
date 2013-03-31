# coding: utf-8

from __future__ import absolute_import

from django.forms.widgets import MultiWidget, TextInput
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse_lazy


class ZipInput(TextInput):
    class Media:
        js = ('cepbrcache/cepbrcache.js',)

    def __init__(self, attrs=None):
        url = reverse_lazy('cepbr:get_cep')
        attrs = {'data-cepbrinput': 'zip', 'data-url': url}
        super(ZipInput, self).__init__(attrs)


class CityInput(TextInput):
    def __init__(self, attrs=None):
        attrs = {'data-cepbrinput': 'city'}
        super(CityInput, self).__init__(attrs)


class StreetInput(TextInput):
    def __init__(self, attrs=None):
        attrs = {'data-cepbrinput': 'street'}
        super(StreetInput, self).__init__(attrs)


class AreaInput(TextInput):
    def __init__(self, attrs=None):
        attrs = {'data-cepbrinput': 'larea'}
        super(AreaInput, self).__init__(attrs)


class UFInput(TextInput):
    def __init__(self, attrs=None):
        attrs = {'data-cepbrinput': 'state'}
        super(UFInput, self).__init__(attrs)


class CepCacheWidget(MultiWidget):

    def __init__(self, attrs=None):
        widgets = (ZipInput, StreetInput, CityInput, AreaInput, UFInput)
        super(CepCacheWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return value.split(',')
        return [None, None, None, None, None]

    def render(self, name, value, attrs=None):
        label_input = '<label for="id_%s">%s</label>'

        widget_labels = [
            label_input % ('%s', 'Cep'),
            label_input % ('%s', 'Logradouro'),
            label_input % ('%s', 'Bairro'),
            label_input % ('%s', 'Cidade'),
            label_input % ('%s', 'Estado'),
        ]

        if self.is_localized:
            for widget in self.widgets:
                widget.is_localized = self.is_localized

        if not isinstance(value, list):
            value = self.decompress(value)

        output = []
        final_attrs = self.build_attrs(attrs)
        id_ = final_attrs.get('id', None)
        for i, widget in enumerate(self.widgets):
            try:
                widget_value = value[i]
            except IndexError:
                widget_value = None
            if id_:
                final_attrs = dict(final_attrs, id='%s_%s' % (id_, i))

            output.append(widget_labels[i] % ('%s_%s' % (name, i)))
            output.append(widget.render(name + '_%s' % i, widget_value, final_attrs))

        return mark_safe(self.format_output(output))
