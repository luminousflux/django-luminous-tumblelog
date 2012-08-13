from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.simple import direct_to_template
from django.contrib.sites.models import get_current_site
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from tumblelog.models import Post, PARENT_MODEL
from tumblelog.forms import form_for_type, ExtendableForm
from tumblelog.settings import POSTS_PER_PAGE
from tumblelog.bookmarklet import generate_bookmarklink
import httplib2

from html2text import html2text
import copy


class PostListView(ListView):
    context_object_name = 'posts'
    paginate_by = POSTS_PER_PAGE

    def get_queryset(self):
        return Post.objects.public()

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context.update({
            'list_view': True,
            'detail_view': False,
        })
        return context


class PostDetailView(DetailView):
    context_object_name = 'post'

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
    response = direct_to_template(request, 'tumblelog/bookmarklet.js', {'site': get_current_site(request)}, mimetype='text/javascript')
    response['Access-Control-Allow-Origin'] = '*'
    return response

@csrf_exempt
def bookmarklet_window(request):
    forms = form_for_type

    templatevars = {'site': get_current_site(request), 'bookmarklink': generate_bookmarklink(request), 'proper': request.method=='POST',}
    if request.method == 'POST':
        from embedly import Embedly

        oembed = None


        url = request.POST['url']
        proper = request.POST.get('proper')
        images = [(x[4:],request.POST[x+'_w'],request.POST[x+'_h'],) for x in request.POST.keys() if x.startswith('img_') and not x[-1] in ('w','h')]
        quote = html2text(request.POST.get('selection',''))
        
        if hasattr(settings,'EMBEDLY_KEY') and not proper:
            client = Embedly(settings.EMBEDLY_KEY)
            try:
                oe = client.oembed(url, maxwidth=None if not hasattr(settings,'EMBEDLY_MAXWIDTH') else settings.EMBEDLY_MAXWIDTH)
                if not oe.error:
                    oembed = oe
            except httplib2.ServerNotFoundError, e:
                pass # Can't connect to server.


        if oembed:
            mode = oembed['type']
        else:
            mode = 'quote' if quote else 'picture' if images else 'link'
        templatevars['url'] = url
        templatevars['images'] = images
        templatevars['quote'] = quote
        initial = {'provider_url': url,'author':request.user,'body':quote}

        def generate_meta(name, parentmeta):
            newmeta = copy.copy(parentmeta)
            newmeta.exclude = copy.copy(parentmeta.exclude) + ['author']
            return newmeta
        formchilds = []
        for name, form in forms.iteritems():
            newcls = type(form.__name__, (form,), {'Meta': generate_meta(name, form._meta)})
            formchilds.append((name,newcls,))

        forms = {}
        for x,y in formchilds:
            init = copy.copy(initial)
            data = None if not proper and oembed and mode == x else request.POST if proper and mode == x else None
            if not proper and oembed and mode==x:
                init.update(oembed.data)
            prefix = x

            print x,init,data
            forms[x] = y(
                    data=data,
                    prefix=prefix,
                    initial=dict(init.items() + {'post_type': x}.items()),
                    instance = Post(author=request.user))
            if not proper and oembed and mode==x:
                try:
                    forms[x].is_valid()
                except ValueError,x:
                    print x
        if PARENT_MODEL:
            for name, form in forms.iteritems():
                form.fields['parent'].queryset = PARENT_MODEL.objects.for_user(request.user)
        if request.POST.get('submit', None):
            mode = request.POST['submit']
            print 'submitted', mode
            try:
                if forms[mode].is_valid():
                    forms[mode].save()
                    templatevars['success'] = True
            except ValueError, e:
                print e
                pass # DAFUQDAFUQ
        templatevars['forms'] = forms
        templatevars['mode'] = mode

    response = direct_to_template(request, 'tumblelog/bookmarklet.html', templatevars)
    response['Access-Control-Allow-Origin'] = '*'
    return response
