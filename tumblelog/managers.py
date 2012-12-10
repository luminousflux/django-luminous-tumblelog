from datetime import datetime
from itertools import islice, chain


from django.db import models
from django.db.models import Q
from django.db.models.query import QuerySet
from django.conf import settings

from django.core.paginator import Paginator

import traceback


class QuerySetChain(object):
    """
    Chains multiple subquerysets (possibly of different models) and behaves as
    one queryset.  Supports minimal methods needed for use with
    django.core.paginator.
    """

    def __init__(self, *subquerysets):
        self.querysets = subquerysets

    def count(self):
        """
        Performs a .count() for all subquerysets and returns the number of
        records as an integer.
        """
        return sum(qs.count() for qs in self.querysets)

    def _clone(self):
        "Returns a clone of this queryset chain"
        return self.__class__(*self.querysets)

    def _all(self):
        "Iterates records in all subquerysets"
        return chain(*self.querysets)

    def __getitem__(self, ndx):
        """
        Retrieves an item or slice from the chained set of results from all
        subquerysets.
        """
        if type(ndx) is slice:
            return list(islice(self._all(), ndx.start, ndx.stop, ndx.step or 1))
        else:
            return islice(self._all(), ndx, ndx+1).next()

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

    def get_page(self, page, posts_per_page=10):
        qs = self
        qs.order_by('published_at')
        pinned = qs.filter(pin_until__isnull=False).filter(pin_until__gte=datetime.now())
        qs2 = qs.exclude(pin_until__isnull=False,pin_until__gte=datetime.now())
        qs3 = QuerySetChain(pinned, qs2)
        return Paginator(qs3,posts_per_page).page(page)

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

