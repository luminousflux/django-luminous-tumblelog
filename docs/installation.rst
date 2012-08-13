Installation
============

[THIS DOES NOT WORK YET]

Installing tumblelog is simple with `pip <http://www.pip-installer.org/en/latest/index.html>`_.

::

    $ pip install django-tumblelog

Quickstart
----------

Add tumblelog to ``INSTALLED APPS`` in your settings module:

::

    INSTALLED_APPS = [
        'tumblelog',
    ]

Create the necessary database tables, using either ``syncdb`` or ``migrate`` (if using `South <http://south.aeracode.org/>`_).

::

    $ python manage.py syncdb
    $ python manage.py migrate tumblelog

Add a :ref:`TUMBLELOG_POST_TYPES <tumblelog_post_types_setting>` setting to your settings module, e.g.

Finally, include the tumblelog URLconf to your ``urls`` module. The regex may be modified as you wish, though the ``tumblelog`` namespace must be maintained.

::

    url(r'^tumblelog/', include('tumblelog.urls', namespace='tumblelog')),

Dependencies
------------

[THIS IS OUTDATED]

Tumblelog has two dependencies:

- `python-oembed <https://github.com/abarmat/python-oembed>`_ 0.2.1
- The latest version of the `Python Imaging Library <http://www.pythonware.com/products/pil/>`_

Source Code
-----------

tumblelog is developed on GitHub, where you can fork the repository, `browse the code and report issues at <https://github.com/luminousflux/django-luminous-tumblelog>`_.

