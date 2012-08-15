from django.db import models
from django.db.models import get_model
from jsonfield import JSONField
import copy

from django.contrib.auth.models import User
from django.conf import settings


from django.conf import settings

from tumblelog.managers import PostManager
from django.template import loader

assert('django_extensions' in settings.INSTALLED_APPS)
assert('crispy_forms' in settings.INSTALLED_APPS)

PARENT_MODEL = get_model(*settings.TUMBLELOG_PARENT_MODEL.split('.')) if hasattr(settings,'TUMBLELOG_PARENT_MODEL') else None

class Post(models.Model):
    post_type = models.CharField(max_length=100, null=False, blank=False)
    author = models.ForeignKey(User, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(null=True, blank=True)
    data = JSONField(blank=True)


    if PARENT_MODEL:
        parent = models.ForeignKey(PARENT_MODEL, null=False, blank=False)

    
    objects = PostManager()

    class Meta:
        ordering = ['-created_at']

    @property
    def slug(self):
        return self.pk

    @property
    def template(self):
        x = loader.select_template(['tumblelog/post/%s.html' % (self.post_type), 'tumblelog/post.html'])
        return x.name

    @models.permalink
    def get_absolute_url(self):
        params = {'id': self.id}
        if PARENT_MODEL:
            params['parent__slug'] = self.parent.slug
        return ('tumblelog:detail', [], params)

    def __unicode__(self):
        return '%s:%s' % (self.post_type, self.id,)

    def save(self,*args,**kwargs):
        super(Post, self).save(*args,**kwargs)
