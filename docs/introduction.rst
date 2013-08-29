============
Introduction
============

smartypants_ is a Python fork of SmartyPants__.

.. _smartypants: https://bitbucket.org/livibetter/smartypants.py
__ SmartyPantsPerl_
.. _SmartyPantsPerl: http://daringfireball.net/projects/smartypants/

smartypants can perform the following transformations:

- Straight quotes (``"`` and ``'``) into “curly” quote HTML entities
- Backticks-style quotes (````like this''``) into “curly” quote HTML entities
- Dashes (``--`` and ``---``) into en- and em-dash entities
- Three consecutive dots (``...`` or ``. . .``) into an ellipsis entity

This means you can write, edit, and save your posts using plain old
ASCII straight quotes, plain dashes, and plain dots, but your published
posts (and final HTML output) will appear with smart quotes, em-dashes,
and proper ellipses.

smartypants does not modify contents in some HTML element, see :ref:`Skipped HTML
Elements <skip-html>`. Typically, these tags are used to display text where
smart quotes and other "smart punctuation" would not be appropriate, such as
source code or example markup.


Quick usage
===========

To use it as a module:

.. code:: python

  import smartypants

  text = '"SmartyPants" is smart, so is <code>smartypants</code> -- a Python port'
  print(smartypants.smartypants(text))

To use the command-line script ``smartypants``:

.. code:: sh

  echo '"SmartyPants" is smart, so is <code>smartypants</code> -- a Python port' | smartypants

Both produce::

  &#8220;SmartyPants&#8221; is smart, so is <code>smartypants</code> &#8212; a Python port


Installation
============

smartypants can be installed via ``pip``::

  $ pip install smartypants
