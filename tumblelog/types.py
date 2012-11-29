from django import forms

POST_TYPES = {
    'photo': {'provider_url': forms.URLField(label='Source URL', required=False),
              'photo': forms.URLField(label='Photo URL'),
              'text': forms.CharField(required=False, widget=forms.Textarea),},
    'video': {'html': forms.CharField(widget=forms.Textarea),
              'text': forms.CharField(widget=forms.Textarea,required=False),},
    'link': {'provider_url': forms.URLField(label='Link'),
             'title': forms.CharField(required=False),
             'text': forms.CharField(widget=forms.Textarea,required=False),},
    'quote': {'provider_url': forms.URLField(label='Source URL', required=False),
              'source': forms.CharField(required=False, label='Source Name'),
              'body': forms.CharField(widget=forms.Textarea),
              'text': forms.CharField(widget=forms.Textarea,required=False),}
}

