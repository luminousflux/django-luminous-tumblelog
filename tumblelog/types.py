from django import forms

POST_TYPES = {
    'photo': {'provider_url': forms.URLField(label='Source URL', required=False),
              'photo': forms.URLField(label='Photo URL')},
    'video': {'html': forms.CharField(widget=forms.Textarea),},
    'link': {'provider_url': forms.URLField(label='Link'),
             'title': forms.CharField(required=False),},
    'quote': {'provider_url': forms.URLField(label='Source URL', required=False),
              'source': forms.CharField(required=False),
              'body': forms.CharField(forms.Textarea),}
}

