A simple and extensible tumblelog engine for Django. Created by Chuck Harmston, released under the `MIT license <https://github.com/chuckharmston/django-tumblelog/blob/master/LICENSE>`_.

`View full documentation <http://django-tumblelog.readthedocs.org/>`_.

--------
Features
--------

* Simple definition of custom post types
* Large stable of contrib post types to get started quickly.

  - Post short text blurbs, long-form articles, links, files, photos, and code snippets.

* oEmbed support, for embedding of 3rd-party media in posts.

  - Post directly from Twitter, Flickr, Instagram, Rdio, SoundCloud, Vimeo, YouTube, and GitHub.

* Optional integration with `django-taggit <http://django-taggit.readthedocs.org/>`_
* Takes full advantage of Django's templating system
* Agnostic of commenting system and markup format.
* Internationalization-ready
* Post scheduling
* Draft posts
* Multi-author support with object-level permissions
* RSS feed

-------------
Release Notes
-------------

Until 1.0, consider this to be beta software with unstable APIs.

0.2
---

*Released on 2012-03-31*

* Adds Twitter web intent URLs to Twitter post type (`commit 01551f2ba1 <https://github.com/chuckharmston/django-tumblelog/commit/01551f2ba140bf6ff1969f3b771c2da9d4b6fda6>`_)
* Creates ``tumblelog.contrib`` (`commit 00deb628f1 <https://github.com/chuckharmston/django-tumblelog/commit/00deb628f1fa073e062eea4a63da29f0e2d66208>`_)
* Adds RSS feed (commits `ed06d0c9f3 <https://github.com/chuckharmston/django-tumblelog/commit/ed06d0c9f309c043926ba8fe7a06dfb99a3453a4>`_, `7a59215a84 <https://github.com/chuckharmston/django-tumblelog/commit/7a59215a848f8a21cdec3628507071b65efd048b>`_, and `5b8cb322d5 <https://github.com/chuckharmston/django-tumblelog/commit/5b8cb322d5e19ca9f2b112b7fb1fdeca4c9cbc29>`_)
* Adds example templates (`commit feba83afaa <https://github.com/chuckharmston/django-tumblelog/commit/feba83afaa4b61453d5b1833b46124fcdb393d42>`_)
* Adds author fields, row-level permissions restricting ability to edit posts a user did not author, and permissions denoting whether a user can edit others' posts/change a post's author.(`commit 2cc2bfda3 <https://github.com/chuckharmston/django-tumblelog/commit/2cc2bfda3eba110d7c40eb184b8e337177031495>`_)
* ``django-taggit`` integration (`commit 8a6ed5d0ea <https://github.com/chuckharmston/django-tumblelog/commit/8a6ed5d0ea38067050b87c8dd62e4436df88c94f>`_)
* Various improvements to documentation

0.1
---

*Released on 2012-03-04*

* First releases