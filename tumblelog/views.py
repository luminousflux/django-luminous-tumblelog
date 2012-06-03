from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from tumblelog.models import Post
from tumblelog.settings import POSTS_PER_PAGE


class PostListView(ListView):
    context_object_name = 'posts'
    paginate_by = POSTS_PER_PAGE

    def get_queryset(self):
        return Post.objects.public().select_generic_related()

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
        return Post.objects.public().select_generic_related()

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context.update({
            'list_view': False,
            'detail_view': True,
        })
        return context
