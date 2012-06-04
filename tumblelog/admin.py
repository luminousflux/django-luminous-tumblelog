from copy import deepcopy

from django.contrib import admin

from tumblelog.settings import EDIT_META, POST_TYPES, USE_TAGGIT
from tumblelog.util import import_model


class PostTypeAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        """
        On new saves, sets the post author to the current user if it wasn't
        already defined.
        """
        if not obj.author:
            obj.author = request.user
        obj.save()

    def get_fieldsets(self, request, obj=None):
        """
        Hook for specifying fieldsets for the add form, modified to only
        display fields inside fieldsets that the user has permission to change.
        """
        if self.declared_fieldsets:
            fieldsets = self.declared_fieldsets
        else:
            form = self.get_form(request, obj)
            fieldsets = form.base_fields.keys() + \
                list(self.get_readonly_fields(request, obj))
        fieldsets = super(PostTypeAdmin, self).get_fieldsets(request, obj=obj)
        fieldsets = deepcopy(fieldsets)
        for fieldset in fieldsets:
            fieldset[1]['fields'] = [field for field in fieldset[1]['fields'] \
                if self.can_change_field(request, obj, field)]
        for fieldset in fieldsets:
            if not fieldset[1]['fields']:
                fieldsets.remove(fieldset)

        return fieldsets

    def get_form(self, request, obj=None):
        """
        Returns a Form class (used by add_view and change_view) modified to
        only include fields the user has permissions to view.
        """
        form = super(PostTypeAdmin, self).get_form(request, obj)
        for field_name, field in form.base_fields.items():
            if not self.can_change_field(request, obj, field_name):
                del form.base_fields[field_name]
        return form

    def can_change_field(self, request, obj, field_name):
        """
        Returns boolean indicating whether the user has necessary permissions to
        view the passed field.
        """
        if field_name == 'author':
            if not request.user.has_perm('tumblelog.change_author'):
                return False
        return True

    def queryset(self, request):
        """
        If the user has permission to edit others' posts,, display all posts in
        the change_view. Otherwise, only display the users posts.
        """
        posts = super(PostTypeAdmin, self).queryset(request)
        if request.user.has_perm('tumblelog.edit_others_posts'):
            return posts
        else:
            return posts.filter(author=request.user)

    def has_change_permission(self, request, obj=None):
        """
        If the user is the author of the post or has the proper permissions,
        they can change this object.
        """
        if not obj or obj.author == request.user or \
            request.user.has_perm('tumblelog.edit_others_posts'):
            return True
        return False

# Dynamically generate admin class from values passed to TumblelogMeta
for post_type in POST_TYPES:
    is_contrib = post_type.startswith('tumblelog.')
    model = import_model(post_type)
    admin_cls = type(
        PostTypeAdmin.__name__,
        (PostTypeAdmin,),
        dict((k, v,) for k, v in model._tumblelog_meta if not k.startswith('_'))
    )

    # Slightly hacky; add taggit manager to the meta fieldset for all the
    # tumblelog.contrib post types
    if post_type and is_contrib and USE_TAGGIT:
        meta_fields = [i for i in admin_cls.fieldsets[1][1]['fields']]
        meta_fields.append('tags')
        admin_cls.fieldsets[1][1]['fields'] = meta_fields

    # Slightly hacky; add meta_description field to the meta fieldset for all
    # the tumblelog.contrib post types
    if post_type and is_contrib and EDIT_META:
        meta_fields = [i for i in admin_cls.fieldsets[1][1]['fields']]
        meta_fields.append('meta_description')
        admin_cls.fieldsets[1][1]['fields'] = meta_fields

    admin.site.register(model, admin_cls)
