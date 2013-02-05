import copy
import hashlib
import requests
import os.path
from easy_thumbnails.files import get_thumbnailer
from datetime import datetime

from tumblelog.managers import PostManager

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import get_model
from django.template import loader
from django.utils.translation import ugettext as _
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.storage import DefaultStorage
from django.template.defaultfilters import slugify


from jsonfield import JSONField
from tumblelog import settings as tumblesettings


assert('django_extensions' in settings.INSTALLED_APPS)
assert('crispy_forms' in settings.INSTALLED_APPS)
assert('easy_thumbnails' in settings.INSTALLED_APPS)

PARENT_MODEL = get_model(*settings.TUMBLELOG_PARENT_MODEL.split('.')) if hasattr(settings,'TUMBLELOG_PARENT_MODEL') else None
KEY_SIZE = settings.TUMBLELOG_KEY_SIZE if hasattr(settings, 'TUMBLELOG_KEY_SIZE') else 30

def get_profile_model():
    return models.get_model(*settings.AUTH_PROFILE_MODULE.split('.'))

class Post(models.Model):
    post_type = models.CharField(_('post type'), max_length=100, null=False, blank=False)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    published_at = models.DateTimeField(_('published at'), null=True, blank=True, auto_now_add=True)
    pin_until = models.DateTimeField(_('pin until'), null=True,blank=True,help_text=_('Leave empty to not pin'))
    data = JSONField(blank=True)

    author = models.ForeignKey(User, null=False, blank=False, verbose_name=_('author'))

    if PARENT_MODEL:
        parent = models.ForeignKey(PARENT_MODEL, null=False, blank=False, verbose_name=_('parent'))

    objects = PostManager()

    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)
        for key in tumblesettings.TUMBLELOG_MIRROR_IMAGEFIELDS:
            if key in self.data and '%s_storagepath'%key in self.data:
                for k,v in tumblesettings.THUMBNAILER.iteritems():
                    setattr(self, u'%s_%s' % (key,k,), lambda: get_thumbnailer(self.data['%s_storagepath' % key]).get_thumbnail(v))

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')

    def save(self,*args,**kwargs):
        for key in tumblesettings.TUMBLELOG_MIRROR_IMAGEFIELDS:
            if key in self.data:
                self.mirror(key)
        super(Post, self).save(*args,**kwargs)

    def mirror(self, key):
        if u'%s_original' % key in self.data:
            return
        url = self.data[key]
        try:
            fd = requests.get(url)
            if 'image' in fd.headers['content-type']:
                img_temp = SimpleUploadedFile(slugify(url), fd.content, fd.headers['content-type'])
                self.data[u'%s_storagepath' % key] = DefaultStorage().save(os.path.join('tumblelog_mirror',slugify(url)), img_temp)
                self.data[key] = DefaultStorage().url(self.data[u'%s_storagepath' % key])
                self.data[u'%s_original' % key] = url
        except Exception, e:
            print 'exception in urlfetching', e

    def __unicode__(self):
        return (u'%s:%s' % (self.post_type, self.id,)) + (u'' if not PARENT_MODEL else u' for %s' % self.parent)

    @models.permalink
    def get_absolute_url(self):
        params = {'id': self.id}
        if PARENT_MODEL:
            params['parent__slug'] = self.parent.slug
        return ('tumblelog:detail', [], params)

    @property
    def slug(self):
        return self.pk

    @property
    def template(self):
        x = loader.select_template(['tumblelog/post/%s.html' % (self.post_type), 'tumblelog/post/base.html'])
        return x.name

    @property
    def is_pinned(self):
        return self.pin_until and self.pin_until > datetime.now()



class ApiKeyProfileMixin(models.Model):
    """required mixin for whatever model is registered as settings.AUTH_PROFILE_MODEL
    """
    _api_key = models.TextField(_('API key'), null=True)

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
