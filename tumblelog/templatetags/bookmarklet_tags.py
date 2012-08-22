from django.template import TemplateDoesNotExist, TemplateSyntaxError
from django.template.loader import get_template
from django.template.loader_tags import BaseIncludeNode
from django import template
register = template.Library()

class ConditionalIncludeTypeletNode(BaseIncludeNode):
    def __init__(self, post_type, *args, **kwargs):
        self.post_type = post_type
        super(ConditionalIncludeTypeletNode, self).__init__(*args, **kwargs)

    def render(self, context):
        post_type = self.post_type.resolve(context) if hasattr(self.post_type, 'resolve') else self.post_type
        try:
            t = get_template('tumblelog/bookmarklet/%s_typelet.html' % post_type)
            return self.render_template(t, context)
        except TemplateDoesNotExist, e:
            return ''


@register.tag('conditional_include_typelet')
def do_conditional_include_typelet(parser, token):
    """
    Loads a template for a post_type and renders it with the current context if it exists. You can pass
    additional context using keyword arguments.

    this looks for 'tumblelog/bookmarklet/{{name}}_typelet.html' templates

    Example::

        {% conditional_include_typelet "name" %}
        {% conditional_include_typelet variable with bar="BAZZ!" baz="BING!" %}

    Use the ``only`` argument to exclude the current context when rendering
    the included template::
    """
    bits = token.split_contents()
    if len(bits) < 2:
        raise TemplateSyntaxError("%r tag takes at least one argument: the name of the template to be included." % bits[0])
    options = {}
    remaining_bits = bits[2:]
    while remaining_bits:
        option = remaining_bits.pop(0)
        if option in options:
            raise TemplateSyntaxError('The %r option was specified more '
                                      'than once.' % option)
        if option == 'with':
            value = token_kwargs(remaining_bits, parser, support_legacy=False)
            if not value:
                raise TemplateSyntaxError('"with" in %r tag needs at least '
                                          'one keyword argument.' % bits[0])
        elif option == 'only':
            value = True
        else:
            raise TemplateSyntaxError('Unknown argument for %r tag: %r.' %
                                      (bits[0], option))
        options[option] = value
    isolated_context = options.get('only', False)
    namemap = options.get('with', {})
    path = bits[1]
    return ConditionalIncludeTypeletNode(path[1:-1] if path[0] in ('"', "'") and path[-1] == path[0] else parser.compile_filter(bits[1]),
                               extra_context=namemap,
                               isolated_context=isolated_context)
