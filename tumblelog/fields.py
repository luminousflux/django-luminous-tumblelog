import requests

from django import forms
from django.conf import settings
from django.utils.translation import ugettext as _


class ImageURLField(forms.URLField):
    def clean(self, value):
        value = super(ImageURLField, self).clean(value)
        if not value:
            return value
        try:
            r = requests.head(value)
            if r.status_code != 200:
                raise forms.ValidationError(_(u'Invalid URL! (%s)') % r.status_code)
            ctype = r.headers['content-type']
            if not 'image' in ctype:
                raise forms.ValidationError(_(u'This is not an image (%s)') % ctype)
        except requests.exceptions.RequestException, e:
            raise forms.ValidationError(_(u'Request error - URL might be invalid! (%s)') % e)
        return value
