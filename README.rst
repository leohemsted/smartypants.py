==============
smartypants.py
==============

.. contents:: **Contents**


Synopsis
========

The original "SmartyPants" is a free web publishing plug-in for Movable Type,
Blosxom, and BBEdit that easily translates plain ASCII punctuation characters
into "smart" typographic punctuation HTML entities.

This software, *smartypants.py*, endeavours to be a functional port of
SmartyPants to Python.


Description
===========

SmartyPants can perform the following transformations:

- Straight quotes ( " and ' ) into "curly" quote HTML entities
- Backticks-style quotes (\`\`like this'') into "curly" quote HTML entities
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

As module
---------

.. code:: python

  import smartypants

  text = '"SmartyPants" is smart, so is <code>smartypants.py</code> -- a Python port'
  print(smartypants.smartyPants(text))

It outputs::

  &#8220;SmartyPants&#8221; is smart, so is <code>smartypants.py</code> &#8212; a Python port


Via CLI
-------

.. code:: sh

  $ echo '"SmartyPants" is smart, so is <code>smartypants.py</code> -- a Python port' | smartypants
  &#8220;SmartyPants&#8221; is smart, so is <code>smartypants.py</code> &#8212; a Python port


Backslash Escapes
=================

If you need to use literal straight quotes (or plain hyphens and
periods), SmartyPants accepts the following backslash escape sequences
to force non-smart punctuation. It does so by transforming the escape
sequence into a decimal-encoded HTML entity:

+--------+-------+-----------+
| Escape | Value | Character |
+========+=======+===========+
| ``\\`` | &#92; | \\        |
+--------+-------+-----------+
| ``\"`` | &#34; | "         |
+--------+-------+-----------+
| ``\'`` | &#39; | '         |
+--------+-------+-----------+
| ``\.`` | &#46; | .         |
+--------+-------+-----------+
| ``\-`` | &#45; | \-        |
+--------+-------+-----------+
| ``\``` | &#96; | \`        |
+--------+-------+-----------+

This is useful, for example, when you want to use straight quotes as
foot and inch marks: 6'2" tall; a 17" iMac.

Options
=======

Numeric values are the easiest way to configure SmartyPants' behavior:

"0"
    Suppress all transformations. (Do nothing.)
"1"
    Performs default SmartyPants transformations: quotes (including
    \`\`backticks'' -style), em-dashes, and ellipses. "``--``" (dash dash)
    is used to signify an em-dash; there is no support for en-dashes.

"2"
    Same as smarty_pants="1", except that it uses the old-school typewriter
    shorthand for dashes:  "``--``" (dash dash) for en-dashes, "``---``"
    (dash dash dash)
    for em-dashes.

"3"
    Same as smarty_pants="2", but inverts the shorthand for dashes:
    "``--``" (dash dash) for em-dashes, and "``---``" (dash dash dash) for
    en-dashes.

"-1"
    Stupefy mode. Reverses the SmartyPants transformation process, turning
    the HTML entities produced by SmartyPants into their ASCII equivalents.
    E.g.  "&#8220;" is turned into a simple double-quote ("), "&#8212;" is
    turned into two dashes, etc.


The following single-character attribute values can be combined to toggle
individual transformations from within the SmartyPants attributes. For
example, to educate normal quotes and em-dashes, but not ellipses or
\`\`backticks'' -style quotes:

.. code:: python

  smartypants.smartyPants(text, '1')

In CLI:

.. code:: sh

  echo "$text" | smartypants -a '1'

"q"
    Educates normal quote characters: (") and (').

"b"
    Educates \`\`backticks'' -style double quotes.

"B"
    Educates \`\`backticks'' -style double quotes and \`single' quotes.

"d"
    Educates em-dashes.

"D"
    Educates em-dashes and en-dashes, using old-school typewriter shorthand:
    (dash dash) for en-dashes, (dash dash dash) for em-dashes.

"i"
    Educates em-dashes and en-dashes, using inverted old-school typewriter
    shorthand: (dash dash) for em-dashes, (dash dash dash) for en-dashes.

"e"
    Educates ellipses.

"w"
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
    regular quotes so SmartyPants can educate them, you should pass the
    following to the smarty_pants attribute:


Caveats
=======

Why You Might Not Want to Use Smart Quotes in Your Weblog
---------------------------------------------------------

For one thing, you might not care.

Most normal, mentally stable individuals do not take notice of proper
typographic punctuation. Many design and typography nerds, however, break
out in a nasty rash when they encounter, say, a restaurant sign that uses
a straight apostrophe to spell "Joe's".

If you're the sort of person who just doesn't care, you might well want to
continue not caring. Using straight quotes -- and sticking to the 7-bit
ASCII character set in general -- is certainly a simpler way to live.

Even if you I *do* care about accurate typography, you still might want to
think twice before educating the quote characters in your weblog. One side
effect of publishing curly quote HTML entities is that it makes your
weblog a bit harder for others to quote from using copy-and-paste. What
happens is that when someone copies text from your blog, the copied text
contains the 8-bit curly quote characters (as well as the 8-bit characters
for em-dashes and ellipses, if you use these options). These characters
are not standard across different text encoding methods, which is why they
need to be encoded as HTML entities.

People copying text from your weblog, however, may not notice that you're
using curly quotes, and they'll go ahead and paste the unencoded 8-bit
characters copied from their browser into an email message or their own
weblog. When pasted as raw "smart quotes", these characters are likely to
get mangled beyond recognition.

That said, my own opinion is that any decent text editor or email client
makes it easy to stupefy smart quote characters into their 7-bit
equivalents, and I don't consider it my problem if you're using an
indecent text editor or email client.


Algorithmic Shortcomings
------------------------

One situation in which quotes will get curled the wrong way is when
apostrophes are used at the start of leading contractions. For example::

  'Twas the night before Christmas.

In the case above, SmartyPants will turn the apostrophe into an opening
single-quote, when in fact it should be a closing one. I don't think
this problem can be solved in the general case -- every word processor
I've tried gets this wrong as well. In such cases, it's best to use the
proper HTML entity for closing single-quotes (``&#8217;``) by hand.


Bugs
====

To file bug reports or feature requests (other than topics listed in the
Caveats section above) please send email to: mailto:smartypantspy@chad.org

If the bug involves quotes being curled the wrong way, please send example
text to illustrate.

To Do list
----------

- Provide a function for use within templates to quote anything at all.


Authors
=======

`John Gruber`_ did all of the hard work of writing this software in Perl for
`Movable Type`_ and almost all of this useful documentation.  `Chad Miller`_
ported it to Python to use with Pyblosxom_.


Additional Credits
==================

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


Copyright and License
=====================

::

  Copyright (c) 2013 Yu-Jie Lin
  Copyright (c) 2004, 2005, 2007, 2013 Chad Miller
  Copyright (c) 2003 John Gruber
  Licensed under the BSD License, for detailed license information, see COPYING

.. _John Gruber: http://daringfireball.net/
.. _Chad Miller: http://web.chad.org/

.. _Pyblosxom: http://roughingit.subtlehints.net/pyblosxom
.. _SmartyPants: http://daringfireball.net/projects/smartypants/
.. _Movable Type: http://www.movabletype.org/
