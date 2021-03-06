from copy import deepcopy

from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.contrib.admin import SimpleListFilter

from tumblelog.models import Post, PARENT_MODEL
from tumblelog.forms import ExtendableForm,form_for_type
from tumblelog.types import POST_TYPES

__all__ = ['PostAdmin', 'admin_classes']

class ParentListFilter(SimpleListFilter):
    title = _('parent')
    parameter_name = 'parent'

    def lookups(self, request, model_admin):
        parents = set([x.parent for x in Post.objects.filter(author=request.user)])
        return [(x.pk,x,) for x in parents]
    def queryset(self, request, queryset):
        return queryset.filter(parent_id=self.value()) if self.value() else queryset

class PostAdmin(admin.ModelAdmin):
    exclude = tuple()
    form = ExtendableForm

    list_filter = ['author'] + [] if not PARENT_MODEL else [ParentListFilter]
admin.site.register(Post, PostAdmin)

admin_classes = []

def queryset_create(name):
    """ lexical closure for PostAdmin.queryset """
    def queryset(self, request):
        qs = super(PostAdmin,self).queryset(request)
        return qs.filter(post_type=name)
    return queryset
def save_model_create(name):
    """ lexical closure for PostAdmin.save_model """
    def save_model(self, request, obj, form, change):
        if not obj.author_id:
            obj.author = request.user
        if not obj.post_type:
            obj.post_type = name
        super(PostAdmin,self).save_model(request, obj,form,change)
    return save_model
def meta_create(name):
    """ lexical closure for PostProxy.Meta """
    class Meta:
        proxy = True
        verbose_name = name
    return Meta

for name, fields in POST_TYPES.iteritems():
    """ create proxy models for each post type """
    form_cls = form_for_type[name]
    admin_cls = type(
        name + PostAdmin.__name__,
        (PostAdmin,),
        {'form': form_cls,
         'queryset': queryset_create(name),
         'save_model': save_model_create(name),
         'exclude': tuple(['post_type','author','data'] + [x for x in PostAdmin.exclude])})
    
    model_cls = type(
        Post.__name__+'Proxy'+name[0].upper()+name[1:],
        (Post,),
        {'__module__': 'tumblelog.models',
         'Meta': meta_create(name),}
        )

    admin_classes.append((model_cls, admin_cls,))

for registration in admin_classes:
    admin.site.register(*registration)
