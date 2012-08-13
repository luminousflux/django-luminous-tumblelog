from django import forms

POST_TYPES = {
    'photo': {'provider_url': forms.URLField(label='url'),},
    'video': {'html': forms.CharField(widget=forms.Textarea),},
    'link': {'provider_url': forms.URLField(label='url'),
             'title': forms.CharField(required=False),},
    'quote': {'provider_url': forms.URLField(label='url'),
              'title': forms.CharField(required=False),
              'body': forms.CharField(forms.Textarea),}
}

