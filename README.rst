==============
smartypants.py
==============

smartypants.py is a Python port of SmartyPants_.

.. _SmartyPants: http://daringfireball.net/projects/smartypants/

.. contents:: **Contents**


Description
===========

SmartyPants can perform the following transformations:

- Straight quotes (``"`` and ``'``) into “curly” quote HTML entities
- Backticks-style quotes (````like this''``) into “curly” quote HTML entities
- Dashes (``--`` and ``---``) into en- and em-dash entities
- Three consecutive dots (``...`` or ``. . .``) into an ellipsis entity

This means you can write, edit, and save your posts using plain old
ASCII straight quotes, plain dashes, and plain dots, but your published
posts (and final HTML output) will appear with smart quotes, em-dashes,
and proper ellipses.

SmartyPants does not modify characters within ``<pre>``, ``<code>``, ``<kbd>``,
``<math>`` or ``<script>`` tag blocks. Typically, these tags are used to
display text where smart quotes and other "smart punctuation" would not be
appropriate, such as source code or example markup.


Installation
============

smartypants.py can be installed vi pip::

  $ pip install smartypants


Usage
=====

Using as module:

.. code:: python

  import smartypants

  text = '"SmartyPants" is smart, so is <code>smartypants.py</code> -- a Python port'
  print(smartypants.smartypants(text))


smartypants.py ships with a command-line script called ``smartypants``, it can be invoked like:

.. code:: sh

  $ echo '"SmartyPants" is smart, so is <code>smartypants.py</code> -- a Python port' | smartypants


Both produce same output::

  &#8220;SmartyPants&#8221; is smart, so is <code>smartypants.py</code> &#8212; a Python port


Backslash Escapes
=================

If you need to use literal straight quotes (or plain hyphens and
periods), SmartyPants accepts the following backslash escape sequences
to force non-smart punctuation. It does so by transforming the escape
sequence into a decimal-encoded HTML entity:

+--------+----------+-------------+
| Escape | Value    | Character   |
+========+==========+=============+
| ``\\`` | ``#92;`` | ``\``       |
+--------+----------+-------------+
| ``\"`` | ``#34;`` | ``"``       |
+--------+----------+-------------+
| ``\'`` | ``#39;`` | ``'``       |
+--------+----------+-------------+
| ``\.`` | ``#46;`` | ``.``       |
+--------+----------+-------------+
| ``\-`` | ``#45;`` | ``-``       |
+--------+----------+-------------+
| ``\``` | ``#96;`` | ``\```      |
+--------+----------+-------------+

This is useful, for example, when you want to use straight quotes as
foot and inch marks: 6'2" tall; a 17" iMac.

Options
=======

smartypants.py only accepts SmartyPants attributes, which are accessible via
``smartypants.Attr``:

``Attr.q``
    Educates normal quote characters: (") and (').

``Attr.b``
    Educates \`\`backticks''-style double quotes.

``Attr.B``
    Educates \`\`backticks''-style double quotes and \`single' quotes.

``Attr.d``
    Educates em-dashes.

``Attr.D``
    Educates em-dashes and en-dashes, using old-school typewriter shorthand:
    (dash dash) for en-dashes, (dash dash dash) for em-dashes.

``Attr.i``
    Educates em-dashes and en-dashes, using inverted old-school typewriter
    shorthand: (dash dash) for em-dashes, (dash dash dash) for en-dashes.

``Attr.e``
    Educates ellipses.

``Attr.w``
    Translates any instance of ``&quot;`` into a normal double-quote character.
    This should be of no interest to most people, but of particular interest
    to anyone who writes their posts using Dreamweaver, as Dreamweaver
    inexplicably uses this entity to represent a literal double-quote
    character. SmartyPants only educates normal quotes, not entities (because
    ordinarily, entities are used for the explicit purpose of representing the
    specific character they represent). The "w" option must be used in
    conjunction with one (or both) of the other quote options ("q" or "b").
    Thus, if you wish to apply all SmartyPants transformations (quotes, en-
    and em-dashes, and ellipses) and also translate ``&quot;`` entities into
    regular quotes so SmartyPants can educate them.

``Attr.s``
    Stupefy mode. Reverses the SmartyPants transformation process, turning
    the HTML entities produced by SmartyPants into their ASCII equivalents.
    E.g.  ``&#8220;`` is turned into a simple double-quote ("), ``&#8212;`` is
    turned into two dashes, etc.

``Attr.set0``
    Suppress all transformations. (Do nothing.)

``Attr.set1`` = ``Attr.q | Attr.b | Attr.d | Attr.e`` (Default)
    Performs default SmartyPants transformations: quotes (including
    \`\`backticks''-style), em-dashes, and ellipses. ``--`` (dash dash)
    is used to signify an em-dash; there is no support for en-dashes.

``Attr.set2`` = ``Attr.q | Attr.b | Attr.D | Attr.e``
    Same as ``Attr.set1``, except that it uses the old-school typewriter shorthand
    for dashes: ``--`` (dash dash) for en-dashes, ``---`` (dash dash dash) for
    em-dashes.

``Attr.set3`` = ``Attr.q | Attr.b | Attr.i | Attr.e``
    Same as ``Attr.set2``, but inverts the shorthand for dashes: ``--`` (dash dash)
    for em-dashes, and ``---`` (dash dash dash) for en-dashes.

``Attr.default`` = ``Attr.set1``
    Default attributes.

To use these attributes, simply using bitwise or:

.. code:: python

  from smartypants import Attr

  attrs = Attr.q | Attr.d
  smartypants.smartypants(text, attrs)

  attrs = Attr.set1 | Attr.w
  smartypants.smartypants(text, attrs)

When using in command-line, use only the attribute names and drop ``set``:

.. code:: sh

  attrs="qd"
  echo "$text" | smartypants -a "$attrs"

  attrs="1w"
  echo "$text" | smartypants -a "$attrs"


Bugs
====

To file bug reports or feature requests, please `open an issue`__.

__ https://bitbucket.org/livibetter/smartypants.py/issues/new

If the bug involves quotes being curled the wrong way, please add example text
to illustrate.


History
=======

`John Gruber`_ did all of the hard work of writing this software in Perl for
`Movable Type`_ and almost all of this useful documentation.  `Chad Miller`_
ported it to Python to use with Pyblosxom_.

.. _John Gruber: http://daringfireball.net/
.. _Movable Type: http://www.movabletype.org/
.. _Chad Miller: http://web.chad.org/
.. _Pyblosxom: http://pyblosxom.github.io/

Portions of the SmartyPants original work are based on Brad Choate's nifty
MTRegex plug-in.  `Brad Choate`_ also contributed a few bits of source code to
this plug-in.  Brad Choate is a fine hacker indeed.

`Jeremy Hedley`_ and `Charles Wiltgen`_ deserve mention for exemplary beta
testing of the original SmartyPants.

`Rael Dornfest`_ ported SmartyPants to Blosxom.

.. _Brad Choate: http://bradchoate.com/
.. _Jeremy Hedley: http://antipixel.com/
.. _Charles Wiltgen: http://playbacktime.com/
.. _Rael Dornfest: http://raelity.org/

It was later packaged for PyPI by Hao Lian.

Since August 2013, smartypants.py has been managed by `Yu-Jie Lin`_ after
contacted Chad Miller and Hao Lian. Lin took the project manager role and the
package ownership on PyPI. It has also officially supported Python 3.

.. _Yu-Jie Lin: http://yjl.im/


Copyright and License
=====================

::

  Copyright (c) 2013 Yu-Jie Lin
  Copyright (c) 2004, 2005, 2007, 2013 Chad Miller
  Copyright (c) 2003 John Gruber
  Licensed under the BSD License, for detailed license information, see COPYING
