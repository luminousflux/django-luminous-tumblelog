from datetime import datetime

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey
from django.db import models
from django.db.models import Q
from django.db.models.query import QuerySet


class PostQuerySet(QuerySet):
    """
    Subclass of QuerySet adding a select_generic_related() method to bulk fetch
    items related via GenericForeignKey.

    Based on http://djangosnippets.org/snippets/1773/
    """

    def select_generic_related(self):
        """
        Parses the queryset, locates each GenericForeignKey field, and
        attaches each related object. Optimizes Django's GenericForeignKey
        loading facilities by only performing a single query for each related
        ContentType object.
        """
        queryset = self._clone()

        gfk_fields = [field for field in self.model._meta.virtual_fields if
            isinstance(field, GenericForeignKey)]

        post_map = {}
        pt_map = {}
        data_map = {}

        for post in queryset:
            for field in gfk_fields:
                ct_field = field.ct_field
                pt_field = self.model._meta.get_field(ct_field).column
                pt_map.setdefault(
                    getattr(post, pt_field),
                    {}
                )[getattr(post, field.fk_field)] = (field.name, post.id)
            post_map[post.id] = post

        for pt_id, posts in pt_map.items():
            if pt_id:
                content_type = ContentType.objects.get_for_id(pt_id)
                post_mgr = content_type.model_class().objects.select_related()
                post_ids = posts.keys()
                pt_queryset = post_mgr.filter(id__in=post_ids).all()
                for post in pt_queryset:
                    gfk_name, item_id = posts[post.id]
                    data_map[(pt_id, post.id)] = post

        for post in queryset:
            for field in gfk_fields:
                if (getattr(post, field.fk_field) != None):
                    ct_field = field.ct_field
                    pt_field = self.model._meta.get_field(ct_field).column
                    post_type = getattr(post, pt_field)
                    pt_field = getattr(post, field.fk_field)
                    post_obj = data_map[(post_type, pt_field)]
                    setattr(post, field.name, post_obj)

        return queryset


class PostManager(models.Manager):
    """
    Custom model manager for Post and BasePostType. Adds filtering methods for
    only returning queued, past, draft, published, private, and public
    (published + past) objects.
    """

    def get_query_set(self):
        "Ensure that all queries use "
        return PostQuerySet(self.model)

    def queued(self):
        "Returns queued posts (i.e. publish date is in the future)"
        return self.get_query_set().filter(date_published__gt=datetime.now())

    def past(self):
        "Returns past posts (i.e. publish date is in the past)"
        return self.get_query_set().filter(date_published__lte=datetime.now())

    def status(self, status_code):
        "Convenience method for filtering objects by the status field."
        return self.get_query_set().filter(status=status_code)

    def draft(self):
        "Returns posts marked as 'Draft'"
        return self.status('d')

    def published(self):
        "Returns posts marked as 'Published'"
        return self.status('p')

    def private(self):
        "Returns private posts (i.e. either future or draft)"
        return self.get_query_set().filter(
            Q(date_published__gt=datetime.now()) | Q(status='d')
        )

    def public(self):
        "Returns public posts (i.e. those both past and published)"
        return self.published() & self.past()
