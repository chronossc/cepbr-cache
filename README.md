cepbr-cache
===========

cepbr-cache aims to be a local cache around excelent https://github.com/maurobaraldi/cepbr app and cep.correiocontrol.com.br API with contribs for many frameworks to make query ceps fun


# Django setup
First you need to install requirements, after you'll need to configure somethings.

# 1. Settings

Put 'cepbrcache' on you installed apps;

```python
# settings.py
INSTALLED_APPS += ['ceprcache']

```
After you need to collect static files;

```python
python manage.py collectstatic

```

# 2. Urls

```python
# urls.py
    url(r'^cep/', include('cepbrcache.contrib.django.urls', namespace='cepbr')),
```
Note: We use the namespace 'cepbr', so don't change that.


# 3. Forms
Has two ways to use on forms:

```python
# forms.py

    # 1 - using the CepCacheField
    from cepbrcache.contrib.django.forms.fields import CepCacheField
    # 2 - using separatted widgets:
    from cepbrcache.contrib.django.forms.widgets import ZipInput, StreetInput

    # first
    class ExampleForm(forms.Form):
        cep = CepCacheField()

    # second
    class ExampleForm(forms.Form):
        zip = forms.CharField(widget=ZipInput())
        street = forms.CharField(widget=StreetInput())
```

Note: CepCacheField is a field using a MultipleWidget(Zip, Street, Area, City, State inputs) and return a CepCache instance.


# 4. Templates
We need to use {{ form.media }}.















