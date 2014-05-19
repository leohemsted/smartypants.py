=====
Usage
=====

Typically, you import :mod:`smartypants` and call the
:func:`smartypants.smartypants` to convert a text, for example:

.. code:: python

  import smartypants

  text = '"SmartyPants" is smart, so is <code>smartypants.py</code> -- a Python port'
  print(smartypants.smartypants(text))

It results::

  &#8220;SmartyPants&#8221; is smart, so is <code>smartypants.py</code> &#8212; a Python port


Attributes
==========

:func:`smartypants.smartypants` accepts processing attributes, which tells it
what need to be converted.

.. seealso:: :class:`smartypants.Attr <smartypants._Attr>` for a list of attributes.

To use these attributes, simply using bitwise *OR* operator, that is ``A | B``:

.. code:: python

  from smartypants import Attr

  attrs = Attr.q | Attr.d
  smartypants.smartypants(text, attrs)

  attrs = Attr.set1 | Attr.w
  smartypants.smartypants(text, attrs)


.. _skip-html:


Skipped HTML elements
=====================

Elements
--------

By default, there are a few HTML elements that :func:`smartypants.smartypants`
do not try to be smart with them:

.. code:: python

  tags_to_skip = ['pre', 'samp', 'code', 'tt', 'kbd', 'script', 'style', 'math']

If you need to change, for example, adding additional tags and remove one of
them:

.. code:: python

  >>> from smartypants import tags_to_skip as tags
  >>> tags.append('a')
  >>> tags.remove('code')
  >>> tags
  ['pre', 'samp', 'tt', 'kbd', 'script', 'style', 'math', 'a']

The :attr:`smartypants.tags_to_skip` is compiled into a regular expression for
being used by :func:`smartypants.smartypants`. You could actually overwrite
:func:`smartypants._tags_to_skip_regex` and return with your own regular
expression.


Comments
--------

HTML comments are always skipped since they are not rendered in browsers.

.. code:: python

  >>> from smartypants import smartypants as sp
  >>> print(sp('<!-- <span>"foobar"</span> -->'))
  <!-- <span>"foobar"</span> -->

.. important::

  Beware of ``--``, which should not or must not be in a HTML comment.

  .. code:: python

    >>> from smartypants import smartypants as sp
    >>> print(sp('<!-- <span>"foo--bar"</span> -->'))
    <!&#8212; <span>&#8221;foo&#8212;bar&#8221;</span> &#8212;>


Backslash escapes
=================

If you need to use literal straight quotes (or plain hyphens and periods), for
example, text like ``6'2"`` may become ``6‘2”``. To avoid such situation, you
can use backslash escapes like ``6\'2\"``.

.. seealso:: :func:`smartypants.process_escapes` for a complete list of backslash escapes.
