from django.template.loader import render_to_string
from django.contrib.sites.models import get_current_site
import urllib

def generate_bookmarklink(request, user=None):
    user = user if user else request.user
    return 'javascript:'+urllib.quote(render_to_string('tumblelog/bookmarklink.js', {'site': get_current_site(request), 'api_key': user.get_profile().api_key()}))
