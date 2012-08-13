django-tumblelog
================

Jason Kottke `defined <http://www.kottke.org/05/10/tumblelogs/>`_ tumblelogs as:

    a quick and dirty stream of consciousness, a bit like a remaindered links style linklog but with more than just links [...] really just a way to quickly publish the "stuff" that you run across every day on the web. [They have] different ways of displaying various types of content...remaindered links, regular posts, book reviews, and movie reviews are all displayed differently.

Perhaps the best implementation of this model is `Tumblr <http://tumblr.com>`_, a simple hosted tumblelog service that allows you to post text snippets, photos, quotes, links, chat logs, audio files, or video files. While an excellent service, it is a bit limiting; post formats are restricted to those seven things. If you would like a standard format to your recipes or code snippets, you're out of luck. 

``django-luminous-tumblelog`` is an attempt to provide more flexibility to this format.

It is based on ``django-tumblelog`` but massively simplified and enhanced by bookmarklet functionality.

Features
--------

* Flexible definition of Post types.

* Bookmarklet support

  - Post directly from In-Browser links

* Takes full advantage of Django's templating system
* Agnostic of commenting system and markup format.
* Internationalization-ready
* Post scheduling
* Draft posts
* RSS feed

User Guide
----------

Installing and using tumblelog:

.. toctree::
   :maxdepth: 2

   installation
   templating
   rss
   configuration
   changelog

