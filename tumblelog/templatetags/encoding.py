from django import template
import json
import base64

register = template.Library()
@register.filter('json')
def do_json(obj):
    return json.dumps(obj)

@register.filter('base64')
def do_base64(string):
    return base64.b64encode(string)
