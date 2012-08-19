from django.conf import settings

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
        print e
        pass # Can't connect to server.
    print oembed
    return oembed
