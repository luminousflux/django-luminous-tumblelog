from django.conf import settings
from django.utils.translation import ugettext as _

POSTS_PER_PAGE = getattr(settings, 'TUMBLELOG_POSTS_PER_PAGE', 10)

# RSS-related
RSS_TITLE = _(getattr(settings, 'TUMBLELOG_RSS_TITLE', ''))
RSS_LINK = getattr(settings, 'TUMBLELOG_RSS_LINK', '')
RSS_DESCRIPTION = _(getattr(settings, 'TUMBLELOG_RSS_DESCRIPTION', ''))
RSS_NUM = getattr(settings, 'TUMBLELOG_RSS_NUM', 20)
