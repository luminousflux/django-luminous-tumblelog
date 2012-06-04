from datetime import datetime, timedelta
import oembed
from urllib2 import HTTPError

from django.contrib.admin import helpers
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext as _

from tumblelog.managers import PostManager
from tumblelog.mixins import PostMetaMixin
from tumblelog.settings import OEMBED_DEFAULT_CACHE_AGE, TEXTFIELD_HELP_TEXT, \
    USE_TAGGIT


class TumblelogMeta(object):
    """
    A special Meta class for BasePostType subclasses; all properties defined
    herein are ultimately added to BasePostType._tumblelog_meta
    """
    raw_id_fields = None
    fields = None
    exclude = None
    fieldsets = None
    form = None
    filter_vertical = None
    filter_horizontal = None
    radio_fields = None
    prepopulated_fields = None
    formfield_overrides = None
    readonly_fields = None
    ordering = None
    list_display = None
    list_display_links = None
    list_filter = None
    list_select_related = None
    list_per_page = None
    list_max_show_all = None
    list_editable = None
    search_fields = None
    date_hierarchy = None
    save_as = None
    save_on_top = None
    paginator = None
    inlines = None
    list_display = ('__str__',)
    list_display_links = ()
    list_filter = ()
    list_select_related = False
    list_per_page = 100
    list_max_show_all = 200
    list_editable = ()
    search_fields = ()
    date_hierarchy = None
    save_as = False
    save_on_top = False
    paginator = Paginator
    inlines = []
    add_form_template = None
    change_form_template = None
    change_list_template = None
    delete_confirmation_template = None
    delete_selected_confirmation_template = None
    object_history_template = None
    actions = []
    action_form = helpers.ActionForm
    actions_on_top = True
    actions_on_bottom = False
    actions_selection_counter = True

    def __init__(self, opts, **kwargs):
        if opts:
            opts = opts.__dict__.items()
        else:
            opts = []
        opts.extend(kwargs.items())

        for key, value in opts:
            setattr(self, key, value)

    def __iter__(self):
        return iter([(k, v) for (k, v) in self.__dict__.items()])


class Post(PostMetaMixin, models.Model):
    """
    A generic post model, consisting of a single generic foreign key and a set
    of fields commonly used to look up posts. This is intended to be used to
    create aggregate querysets of all subclasses of BasePostType.
    """
    post_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    fields = generic.GenericForeignKey('post_type', 'object_id')
    author = models.ForeignKey(User, blank=True, null=True)
    slug = models.SlugField(_('Slug'),
        max_length=64,
        help_text=_('Used to construct the post\'s URL'),
        unique=True,
    )

    objects = PostManager()

    class Meta:
        app_label = 'tumblelog'
        ordering = ['-date_published']
        permissions = (
            ('change_author', 'Can change the author of a post'),
            ('edit_others_posts', 'Can edit others\' posts'),
        )

    def __unicode__(self):
        return '%s (%s)' % (self.fields.title, self.fields.__class__.__name__,)

    @models.permalink
    def get_absolute_url(self):
        return ('tumblelog:detail', [], {'slug': self.fields.slug})

    @property
    def post_type_name(self):
        if self.fields:
            return slugify(self.fields.__class__.__name__)
        return None


class PostTypeMetaclass(models.base.ModelBase):
    """
    Metaclass for BasePostType models.
    """
    def __new__(cls, name, bases, attrs):
        """
        Creates a TumblelogMeta instance, accessible as obj._tumblelog_meta in
        any BasePostType subclasses.
        """
        opts = TumblelogMeta(attrs.pop('TumblelogMeta', None))
        attrs['_tumblelog_meta'] = opts

        # Make public pointer for templating
        def get_tumblelog_meta(self):
            return self._tumblelog_meta
        attrs['tumblelog_meta'] = get_tumblelog_meta

        return super(PostTypeMetaclass, cls).__new__(cls, name, bases, attrs)


class BasePostType(PostMetaMixin, models.Model):
    """
    Abstract base class whose subclasses carry the constituent fields of each
    post type.
    """
    title = models.CharField(_('Title'), max_length=256)
    author = models.ForeignKey(User, blank=True, null=True)
    slug = models.SlugField(_('Slug'),
        max_length=64,
        help_text=_('Used to construct the post\'s URL'),
        unique=True
    )
    post = generic.GenericRelation(Post, content_type_field='post_type', \
        object_id_field='object_id')
    meta_description = models.TextField(_('Meta Description'),
        blank=True,
        null=True,
        editable=True,
        help_text=_('Recommended length: 150-160 characters'),
    )

    __metaclass__ = PostTypeMetaclass

    class Meta:
        abstract = True
        ordering = ['-date_published']

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return self.post.all()[0].get_absolute_url()

    def clean_fields(self, exclude):
        """
        Ensures that multiple posts do not share a slug.
        """
        super(BasePostType, self).clean_fields(exclude)

        errors = {}
        matching_post = None
        own_post = None
        SLUG_EXISTS = [_('A post with this slug already exists.')]

        try:
            matching_post = Post.objects.get(slug=self.slug)
        except Post.DoesNotExist:
            pass
        else:
            try:
                own_post = self.post.all()[0]
            except IndexError:
                if matching_post:
                    errors['slug'] = SLUG_EXISTS
            else:
                if matching_post != own_post:
                    errors['slug'] = SLUG_EXISTS

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        """
        Overrides save method to either creates or updates the correspondant
        Post object when object is saved.
        """
        super(BasePostType, self).save(*args, **kwargs)
        content_type = ContentType.objects.get_for_model(self)
        post, created = Post.objects.get_or_create(
            post_type=content_type,
            object_id=self.id
        )
        post.status = self.status
        post.date_added = self.date_added
        post.date_modified = self.date_modified
        post.date_published = self.date_published
        post.slug = self.slug
        post.author = self.author
        post.save()

    @property
    def post_template(self):
        return 'tumblelog/post/%s.html' % slugify(self.__class__.__name__)

    @property
    def rss_template(self):
        return [
            'tumblelog/rss/%s.html' % slugify(self.__class__.__name__),
            self.post_template,
        ]


# Add the django-taggit manager, if taggit is installed
if USE_TAGGIT:
    from taggit.managers import TaggableManager
    taggit_manager = TaggableManager()
    taggit_manager.contribute_to_class(BasePostType, 'tags')


class BaseOembedPostType(BasePostType):
    """
    Abstract post type base classes whose subclasses retrieve data from an
    oEmbed endpoint.
    """
    caption = models.TextField(_('Caption'),
        blank=True,
        null=True,
        help_text=TEXTFIELD_HELP_TEXT
    )
    version = models.CharField(_('oEmbed Version'), max_length=3, null=True, \
        blank=True, editable=True)
    provider_name = models.CharField(_('oEmbed Provider Name'), \
        max_length=128, blank=True, null=True, editable=True)
    provider_url = models.CharField(_('oEmbed Provider URL'), max_length=512, \
        blank=True, null=True, editable=True)
    cache_age = models.IntegerField(_('Cache Age'), \
        default=OEMBED_DEFAULT_CACHE_AGE)
    date_updated = models.DateTimeField(_('Last Retrieved'), null=True, \
        blank=True, editable=True)

    oembed_map = (
        'version',
        'provider_name',
        'provider_url',
    )
    oembed_endpoint = None
    oembed_schema = None

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super(BaseOembedPostType, self).__init__(*args, **kwargs)
        if self.pk:
            expiry = timedelta(seconds=self.cache_age) + self.date_updated
            if datetime.now() > expiry:
                self.oembed_update()

    def oembed_consumer(self):
        consumer = oembed.OEmbedConsumer()
        endpoint = oembed.OEmbedEndpoint(
            self.oembed_endpoint,
            self.oembed_schema,
        )
        consumer.addEndpoint(endpoint)
        return consumer

    @property
    def oembed_resource(self):
        return None

    @property
    def oembed_endpoint_params(self):
        return {}

    def oembed_update(self):
        self.date_updated = datetime.now()
        response = self.oembed_retrieve()
        self.oembed_map_values(response)

    def oembed_retrieve(self, suppress_http_errors=True):
        consumer = self.oembed_consumer()
        try:
            return consumer.embed(self.oembed_resource, 'json', \
                **self.oembed_endpoint_params)
        except HTTPError, e:
            if not suppress_http_errors:
                raise e

    def oembed_map_values(self, response):
        for mapping in self.oembed_map:
            try:
                prop, field = mapping
            except ValueError:
                prop, field = mapping, mapping
            finally:
                if hasattr(self, field):
                    value = self.oembed_clean_value(field, response[prop])
                    setattr(self, field, value)

    def oembed_clean_value(self, key, value):
        return value

    def save(self, *args, **kwargs):
        self.oembed_update()
        super(BaseOembedPostType, self).save(*args, **kwargs)


class BaseOembedPhoto(BaseOembedPostType):
    width = models.IntegerField(_('Width'), blank=True, null=True, \
        editable=False)
    height = models.IntegerField(_('Height'), blank=True, null=True, \
        editable=False)
    image_url = models.URLField(_('Image URL'), blank=True, null=True, \
        editable=False)

    class Meta:
        abstract = True

    oembed_map = (
        'version',
        'provider_name',
        'provider_url',
        'width',
        'height',
        ('url', 'image_url',)
    )


class BaseOembedVideo(BaseOembedPostType):
    width = models.IntegerField(_('Width'), blank=True, null=True, \
        editable=False)
    height = models.IntegerField(_('Height'), blank=True, null=True, \
        editable=False)
    embed = models.TextField(_('Embed Code'), blank=True, null=True, \
        editable=False)

    class Meta:
        abstract = True

    oembed_map = (
        'version',
        'provider_name',
        'provider_url',
        'width',
        'height',
        ('html', 'embed',),
    )


class BaseOembedLink(BaseOembedPostType):
    """

    """
    class Meta:
        abstract = True


class BaseOembedRich(BaseOembedPostType):
    width = models.IntegerField(_('Width'), blank=True, null=True, \
        editable=False)
    height = models.IntegerField(_('Height'), blank=True, null=True, \
        editable=False)
    embed = models.URLField(_('Embed Code'), blank=True, null=True, \
        editable=False)

    class Meta:
        abstract = True

    oembed_map = (
        'version',
        'provider_name',
        'provider_url',
        'width',
        'height',
        ('html', 'embed',)
    )
