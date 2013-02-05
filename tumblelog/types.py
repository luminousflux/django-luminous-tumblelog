from django import forms
from tumblelog.fields import ImageURLField

POST_TYPES = {
    'photo': {'url': forms.URLField(label='Source URL', required=False),
              'photo': ImageURLField(label='Photo URL'),
              'text': forms.CharField(required=False, widget=forms.Textarea),},
    'video': {'html': forms.CharField(widget=forms.Textarea),
              'text': forms.CharField(widget=forms.Textarea,required=False),},
    'link': {'url': forms.URLField(label='Link'),
             'title': forms.CharField(required=False),
             'text': forms.CharField(widget=forms.Textarea,required=False),},
    'quote': {'url': forms.URLField(label='Source URL', required=False),
              'source': forms.CharField(required=False, label='Source Name'),
              'body': forms.CharField(widget=forms.Textarea),
              'text': forms.CharField(widget=forms.Textarea,required=False),}
}
