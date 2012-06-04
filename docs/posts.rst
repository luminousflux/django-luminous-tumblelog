====================
Posts and Post Types
====================

As tumblelogs are comprised of a stream of posts, each with a unique strucutre and schema, it is impractical for a single model to represent all types of posts. tumblelog allows you to develop :ref:`separate models for each post type <baseposttype_class>` while maintaining the ability to :ref:`query all posts at a time <post_class>`, regardless of the post type.

.. _baseposttype_class:

------------
BasePostType
------------

Post types are subclasses of ``tumblelog.models.base.BasePostType``, which is itself a subclass of Django's ``db.models.Model``. Let's look at an example post type for recipes, which might be defined in the ``models`` module of an app called ``recipes``:

::

    from django.db import models
    from django.utils.translation import ugettext as _

    from tumblelog.models.base import BasePostType

    class Recipe(BasePostType):
        """
        Post type for a recipe.
        """
        intro = models.TextField(_('Introduction'))
        prep_time = models.CharField(_('Preparation Time'), max_length=128)
        cook_time = models.CharField(_('Cooking Time'), max_length=128)
        recipe_yield = models.CharField(_('Yield'), max_length=128)
        ingredients = models.TextField(_('Ingredients'))
        directions = models.TextField(_('Directions'))

        class TumblelogMeta:
            prepopulated_fields = {
                'slug': ('title',)
            }

In addition to fields, you may add model methods, custom managers, or a ``Meta`` inner class. Anything you can do with regular Django models is fair game.

You should not create a ``ModelAdmin`` for post type classes. Instead, you can define ``ModelAdmin`` properties on inner class ``TumblelogMeta`` (as is done for ``prepopulated_fields`` in the example). These are, in turn, used to dynamically generate a ``ModelAdmin``.

Fields
------

``BasePostType`` provides subclasses with each of these fields:

- ``slug`` - used to construct the URL
- ``title`` - self-explanatory
- ``status`` - defines whether a post is draft or published
- ``date_added`` - automatically created when a post is first added
- ``date_modified`` - automatically updated when a post is saved
- ``date_published`` - defines the date and time when a post is published
- ``meta_description`` - a value for use in the ``<meta type="description" />`` tag

Properties
----------

These properties are available to each ``BasePostType`` subclass:

- ``is_draft`` - boolean, indicates if a post is marked as draft
- ``is_published`` - boolean, indicates if a post is marked as published
- ``is_past`` - boolean, indicates if a post's ``publication_date`` is in the past
- ``is_queued`` - boolean, indicates if a post's ``publication_date`` is in the future (i.e. a scheduled post)
- ``is_public`` - boolean, indicates whether a post is publicly visible (i.e. both ``is_past`` and ``is_published`` are True)
- ``post`` - Post object, a GenericRelation reference to the object's associated :ref:`Post object <post_class>`.
- ``post_template`` - the :ref:`template specific to the post type <post_type_templates>`, suitable for use as the parameter value of the `{% include %} <https://docs.djangoproject.com/en/dev/ref/templates/builtins/#include>`_ tag.

.. _post_class:

----
Post
----

When an instance of a post type is first saved, a corresponding ``Post`` object is created. ``Post`` objects contain a `generic foreign key <https://docs.djangoproject.com/en/dev/ref/contrib/contenttypes/#generic-relations>`_ to an instance of a post type, allowing you to query all post types at once.

::

    >>> from tumblelog.models import Post
    >>> Post.objects.public()
    [<Post: Deboning Pony Legs (Text)>, <Post: Crostini with Pony Tartare (Recipe)>, <Post: Pony Au Poivre (Recipe)>, <Post: Pony Stew with Dried Plums (Recipe)>]
 
Note that the query returned instances of both `Text` and `Recipe` post types. 

Fields
------

Each time a post type object is saved, the values of the ``slug``, ``status``, ``date_published``, ``date_added``, and ``date_modified`` fields are copied from the object to its associated Post object, allowing `field lookups <https://docs.djangoproject.com/en/dev/topics/db/queries/#field-lookups>`_ of each of these fields:

- ``slug`` - used to construct the URL
- ``status`` - defines whether a post is draft or published
- ``date_added`` - automatically created when a post is first added
- ``date_modified`` - automatically updated when a post is saved
- ``date_published`` - defines the date and time when a post is published

Properties
----------

- ``is_draft`` - boolean, indicates if a post is marked as draft
- ``is_published`` - boolean, indicates if a post is marked as published
- ``is_past`` - boolean, indicates if a post's ``publication_date`` is in the past
- ``is_queued`` - boolean, indicates if a post's ``publication_date`` is in the future (i.e. a scheduled post)
- ``is_public`` - boolean, indicates whether a post is publicly visible (i.e. both ``is_past`` and ``is_published`` are True)
- ``fields`` - instance of a :ref:`BasePostType <baseposttype_class>` subclass, a GenericForeignKey
- ``post_type_name`` - a slugified version of the post type class' name, suitable for use as the value of an HTML class attribute

Manager
--------------

``Post``'s default manager is extended to include the following methods:

- ``status(status_code)`` - Convenience method for filtering objects by the status field specified in the parameter (a string; either 'd' or 'p')
- ``draft()`` - Returns posts marked as draft
- ``published()`` - Returns posts marked as published
- ``queued()`` - Returns queued posts (i.e. publish date is in the future)
- ``past()`` - Returns past posts (i.e. publish date is in the past)
- ``private()`` - Returns private posts (i.e. either future or draft)"
- ``public()`` - Returns public posts (i.e. those both past and published)
