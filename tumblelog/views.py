from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.simple import direct_to_template
from django.contrib.sites.models import get_current_site
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.conf import settings
from operator import itemgetter

from tumblelog.models import Post, PARENT_MODEL, get_profile_model
from tumblelog.forms import form_for_type, ExtendableForm
from tumblelog.settings import POSTS_PER_PAGE
from tumblelog.bookmarklet import generate_bookmarklink
import httplib2

from html2text import html2text

from tumblelog import embedly_support

import copy
import json
import base64


class PostListView(ListView):
    context_object_name = 'posts'
    paginate_by = POSTS_PER_PAGE
    template_name = 'tumblelog/post_list.html'

    def get_queryset(self):
        return Post.objects.filter(**self.kwargs).timeline()

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context.update({
            'list_view': True,
            'detail_view': False,
        })
        return context


class PostDetailView(DetailView):
    context_object_name = 'post'
    template_name_field = 'template'

    def get_queryset(self):
        return Post.objects.public()

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context.update({
            'list_view': False,
            'detail_view': True,
        })
        return context

def bookmarklet(request):
    response = direct_to_template(request, 'tumblelog/bookmarklet.js', {'site': get_current_site(request), 'api_key': request.GET['api_key']}, mimetype='text/javascript')
    response['Access-Control-Allow-Origin'] = '*'
    return response

@csrf_exempt
def bookmarklet_window(request):
    forms = form_for_type

    user = get_profile_model().get_by_api_key(request.GET['api_key']).user
    templatevars = {'site': get_current_site(request), 'bookmarklink': generate_bookmarklink(request, user), 'proper': request.method=='POST',
                    'typeimages': hasattr(settings,'TUMBLELOG_TYPEIMAGES') and settings.TUMBLELOG_TYPEIMAGES, 'apiuser': user,
                    }
    if request.method == 'POST':
        oembed = None

        url = request.POST['url']
        proper = request.POST.get('proper')
        images = [(request.POST[x],request.POST[x+'_w'],request.POST[x+'_h'],) for x in request.POST.keys() if x.startswith('img_') and not x[-1] in ('w','h')]
        images.sort(key=itemgetter(2))
        images = json.loads(base64.b64decode(request.POST['images'])) if request.POST.get('images',None) else images
        quote = html2text(request.POST.get('selection',''))

        if not proper:
            oembed = embedly_support.get_info_if_active(url)

        if oembed:
            mode = oembed['type']
        else:
            mode = 'quote' if quote else 'picture' if images else 'link'

        mode = request.POST['submit'] if request.POST.get('submit', None) else mode

        templatevars['url'] = url
        templatevars['images'] = images
        templatevars['quote'] = quote
        templatevars['api_key'] = user.get_profile().api_key()
        initial = {'url': url,'author':user,'body':quote}
        def generate_meta(name, parentmeta):
            newmeta = copy.copy(parentmeta)
            newmeta.exclude = (copy.copy(parentmeta.exclude) or []) + ['author','post_type','data']
            return newmeta
        formchilds = []
        for name, form in forms.iteritems():
            newcls = type(form.__name__, (form,), {'Meta': generate_meta(name, form._meta)})
            formchilds.append((name,newcls,))

        forms = {}
        for x,y in formchilds:
            init = copy.copy(initial)
            data = None if not proper and oembed and mode == x else request.POST if proper and mode == x else None
            if oembed and mode==x:
                init.update(oembed.data)
            prefix = x

            forms[x] = y(
                    data,
                    prefix=prefix,
                    initial=dict(init.items() + {'post_type': x}.items()),
                    instance = Post(author=user))
            if not proper and oembed and mode==x:
                try:
                    forms[x].is_valid()
                except ValueError,x:
                    print x
        if PARENT_MODEL:
            for name, form in forms.iteritems():
                form.fields['parent'].queryset = PARENT_MODEL_GET().objects.for_user(user)
        if request.POST.get('submit', None):
            mode = request.POST['submit']
            form = forms[mode]
            if form.instance:
                form.instance.post_type = mode
            try:
                form.full_clean()
                if form.is_valid():
                    form.save()
                    templatevars['success'] = True
            except ValueError, e:
                pass # if value errors occur here, they should have been caught by form validation.
        templatevars['forms'] = forms
        templatevars['mode'] = mode

    response = direct_to_template(request, 'tumblelog/bookmarklet.html', templatevars)
    response['Access-Control-Allow-Origin'] = '*'
    return response
