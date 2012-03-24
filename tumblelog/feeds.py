from django.contrib.syndication.views import Feed
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string

from tumblelog.models import Post
from tumblelog.settings import RSS_TITLE, RSS_LINK, RSS_DESCRIPTION, RSS_NUM


class PostFeed(Feed):
    """
    RSS feed of all public posts
    """
    title = RSS_TITLE
    description = RSS_DESCRIPTION
    link = RSS_LINK

    def items(self):
        return Post.objects.public()[:RSS_NUM]

    def item_title(self, item):
        return item.fields.title

    def item_link(self, item):
        return item.get_absolute_url()

    def item_description(self, item):
        return render_to_string(item.fields.post_template, {
            'post': item,
            'obj': item,
            'post_type': slugify(item.fields.__class__.__name__),
            'list_view': False,
            'detail_view': True,
        })

    def item_pubdate(self, item):
        return item.date_published
