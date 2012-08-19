from django.conf import settings
import logging

logger = logging.getLogger('django')

__all__ = ('ACTIVE', 'get_info',)

ACTIVE = False
try:
    from embedly import Embedly
    ACTIVE = True
except Exception, e:
    print e

ACTIVE = ACTIVE and hasattr(settings,'EMBEDLY_KEY') and settings.EMBEDLY_KEY

def get_info_if_active(url):
    oembed = None
    if not ACTIVE:
        return oembed
    client = Embedly(settings.EMBEDLY_KEY)
    try:
        oe = client.oembed(url, maxwidth=None if not hasattr(settings,'EMBEDLY_MAXWIDTH') else settings.EMBEDLY_MAXWIDTH)
        if not oe.error:
            oembed = oe
    except httplib2.ServerNotFoundError, e:
        pass # Can't connect to server.
    except httplib2.HttpLib2Error, e:
        logger.warning('tumblelog: %s' % e)
        pass
    return oembed
