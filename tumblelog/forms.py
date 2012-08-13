from django import forms
from tumblelog.models import Post
from tumblelog.types import POST_TYPES

class ExtendableForm(forms.ModelForm):
    post_type = forms.fields.Field(widget=forms.widgets.HiddenInput())

    class Meta:
        model = Post
        exclude = ['data',]

    def __init__(self, *args, **kwargs):
        initial = {}
        if 'initial' in kwargs:
            initial = kwargs['initial']
        if 'instance' in kwargs:
            instance = kwargs['instance']
            for key, value in (instance.data or {}).iteritems():
                initial[key] = value
        kwargs['initial'] = initial
        return super(ExtendableForm, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        cleaned_data = super(ExtendableForm,self).clean(*args,**kwargs)
        fields = [x.name for x in self.Meta.model._meta.fields]
        result = {}
        for field in self.fields:
            if field in fields:
                result[field] = cleaned_data.get(field,None)
            else:
                if not result.get('data', None):
                    result['data'] = {}
                result['data'][field] = cleaned_data.get(field,None)
        return result

    def save(self, *args, **kwargs):
        instance = super(ExtendableForm, self).save(*args, **kwargs)
        instance.data = self.cleaned_data['data']
        if not kwargs.get('commit',None)==False:
            instance.save()
        return instance

form_for_type = {}
for name, fields in POST_TYPES.iteritems():
    form_cls = type(
        name + ExtendableForm.__name__,
        (ExtendableForm,),
        dict(
            fields.iteritems()
            )
        )
    form_for_type[name] = form_cls
