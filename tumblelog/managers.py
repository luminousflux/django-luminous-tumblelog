from datetime import datetime

from django.db import models
from django.db.models import Q
from django.db.models.query import QuerySet
from django.conf import settings

import traceback

class PostQuerySet(QuerySet):
    def queued(self):
        "Returns queued posts (i.e. publish date is in the future)"
        return self.filter(published_at__gt=datetime.now())

    def past(self):
        "Returns past posts (i.e. publish date is in the past)"
        return self.filter(published_at__lte=datetime.now())

    def published_at(self):
        "Returns posts marked as 'Published'"
        return self.filter(published_at__isnull=False)

    def private(self):
        "Returns private posts (i.e. either future or draft)"
        return self.filter(
            Q(published_at__gt=datetime.now())
        )

    def public(self):
        "Returns public posts (i.e. those both past and published_at)"
        return self.published_at() & self.past()

    if hasattr(settings, 'TUMBLELOG_PARENT_MODEL'):
        def for_parent(self, parent):
            return self.filter(parent=parent)



class PostManager(models.Manager):
    """
    Custom model manager for Post and BasePostType. Adds filtering methods for
    only returning queued, past, draft, published_at, private, and public
    (published_at + past) objects.
    """

    def get_query_set(self):
        return PostQuerySet(self.model)

    def __getattr__(self, name):
        if name.startswith('__'):
            return getattr(super(PostManager, self), name)
        return getattr(self.get_query_set(), name)
