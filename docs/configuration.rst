Configuration
=============

tumblelog may be configured with the following settings


.. _tumblelog_post_types_setting:

TUMBLELOG_WIDTH
---------------

Optional; an integer indicating the default width content should have. Only used for embed.ly lookups for now.

Default: ``640``

.. _tumblelog_rss_title_setting:

TUMBLELOG_RSS_TITLE
-------------------

Optional, but recommended; the tumblelog's name, only used in the RSS feed's <title> element.

Default: ``''``

::

    TUMBLELOG_RSS_TITLE = 'five thirty eight'


.. _tumblelog_rss_description_setting:

TUMBLELOG_RSS_DESCRIPTION
-------------------------

Optional, but recommended; a description of the tumblelog, only used in the RSS feed's <description> element.

Default: ``''``

::

    TUMBLELOG_RSS_DESCRIPTION = 'Rigorous analysis of politics, polling, public affairs, sports, science and culture, largely through statistical means.'

.. _tumblelog_rss_link_setting:

TUMBLELOG_RSS_LINK
------------------

Optional, but recommended; the tumblelog's primary URL, used to describe the blog in the RSS feed's <link> element.

Default: ``''``

::

    TUMBLELOG_RSS_LINK = 'http://fivethirtyeight.blogs.nytimes.com'

.. _tumblelog_rss_num_setting:

TUMBLELOG_RSS_NUM
-----------------

Optional; the number of recent posts to include in the RSS feed. 

Default: ``20``

::

    TUMBLELOG_RSS_NUM = 15

.. _embedly_key_setting:

EMBEDLY_KEY
-----------

Optional; the key the bookmarklet uses for embed.ly lookups

Default: ``None``

::

    EMBEDLY_KEY = 'asdf'

