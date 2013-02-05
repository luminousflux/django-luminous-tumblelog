from django.conf import settings
from django.utils.translation import ugettext as _

POSTS_PER_PAGE = getattr(settings, 'TUMBLELOG_POSTS_PER_PAGE', 10)

TUMBLELOG_MIRROR_IMAGEFIELDS = getattr(settings, 'TUMBLELOG_MIRROR_IMAGEFIELDS', ['photo'])

# RSS-related
RSS_TITLE = _(getattr(settings, 'TUMBLELOG_RSS_TITLE', ''))
RSS_LINK = getattr(settings, 'TUMBLELOG_RSS_LINK', '')
RSS_DESCRIPTION = _(getattr(settings, 'TUMBLELOG_RSS_DESCRIPTION', ''))
RSS_NUM = getattr(settings, 'TUMBLELOG_RSS_NUM', 20)
MAXWIDTH = getattr(settings, 'TUMBLELOG_MAXWIDTH', getattr(settings, 'EMBEDLY_MAXWIDTH', 800))

THUMBNAILER = getattr(settings, 'THUMBNAIL_ALIASES', {}).get('thumblelog', {
    'small': {'size': (MAXWIDTH, MAXWIDTH*3,)}
    })
