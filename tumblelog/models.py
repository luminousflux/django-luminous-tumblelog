import copy

from tumblelog.managers import PostManager

from django.conf import settings
from django.db import models
from django.db.models import get_model
from django.contrib.auth.models import User
from django.template import loader

from jsonfield import JSONField

from datetime import datetime
import hashlib

assert('django_extensions' in settings.INSTALLED_APPS)
assert('crispy_forms' in settings.INSTALLED_APPS)

PARENT_MODEL = get_model(*settings.TUMBLELOG_PARENT_MODEL.split('.')) if hasattr(settings,'TUMBLELOG_PARENT_MODEL') else None
KEY_SIZE = settings.TUMBLELOG_KEY_SIZE if hasattr(settings, 'TUMBLELOG_KEY_SIZE') else 30

def get_profile_model():
    return models.get_model(*settings.AUTH_PROFILE_MODULE.split('.'))

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


class ApiKeyProfileMixin(models.Model):
    """required mixin for whatever model is registered as settings.AUTH_PROFILE_MODEL
    """
    _api_key = models.TextField(null=True)

    class Meta:
        abstract = True

    def api_key(self):
        if not self._api_key:
            unique = False
            api_key = None
            while not unique:
                now = datetime.utcnow()
                api_key = hashlib.md5('%s-%s' % (self.user.email, now)).hexdigest()[:KEY_SIZE]
                unique = (self.__class__._default_manager.filter(_api_key=api_key).count() == 0)
            self._api_key = api_key
            self.save()
        return self._api_key

    @classmethod
    def get_by_api_key(cls, api_key):
        return cls._default_manager.get(_api_key=api_key)
