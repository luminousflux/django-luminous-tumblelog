from django.conf.urls.defaults import *

from tumblelog.feeds import PostFeed
from tumblelog.views import PostDetailView, PostListView, bookmarklet, bookmarklet_window

from tumblelog.models import PARENT_MODEL

urlpatterns = patterns('tumblelog.views',
    url(r'^bookmarklet.js/$', bookmarklet, name="bookmarklet.js"),
    url(r'^bookmarklet.html/$', bookmarklet_window, name="bookmarklet.html"),
    url(r'^(?P<parent__slug>.+)/(?P<pk>.+)/$' if PARENT_MODEL else r'^(?P<pk>.+)/$', PostDetailView.as_view(), name="detail"),
    url(r'^(?P<parent__slug>.+)/$' if PARENT_MODEL else r'^$', PostListView.as_view(), name="list"),
    url(r'^feed/$', PostFeed(), name="feed"),
)
