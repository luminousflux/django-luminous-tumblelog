from django import forms
from tumblelog.models import Post
from tumblelog.types import POST_TYPES

_priority_fields = ['parent']

class ExtendableForm(forms.ModelForm):
    class Meta:
        model = Post

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

    def get_fields(self):
        fields = self._fields
        sorter = lambda x,y: 0 if (x in _priority_fields == y in _priority_fields) else -1 if x in _priority_fields else 1
        fields.keyOrder.sort(cmp=sorter)
        return fields
    def set_fields(self, value):
        self._fields = value
    def del_fields(self):
        del self._fields

    fields = property(get_fields, set_fields, del_fields)
    _fields = None

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
