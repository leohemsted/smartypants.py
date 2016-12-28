#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) 2013, 2014, 2016 Yu-Jie Lin
# Copyright (c) 2004, 2005, 2007, 2013 Chad Miller
# Copyright (c) 2003 John Gruber
# Licensed under the BSD License, for detailed license information, see COPYING

"""
smartypants module
==================

:func:`smartypants` is the core of smartypants module.
"""

__author__ = 'Yu-Jie Lin'
__author_email__ = 'livibetter@gmail.com'
__version__ = '2.0.0'
__license__ = 'BSD License'
__url__ = 'https://bitbucket.org/livibetter/smartypants.py'
__description__ = 'Python with the SmartyPants'

import re


class _Attr(object):
    """
    class for instantiation of module attribute :attr:`Attr`.
    """
    q = 1 << 0
    """
    flag for normal quotes (``"``) and (``'``) to curly ones.

    .. seealso:: :func:`convert_quotes`
    """

    b = 1 << 1
    """
    flag for double quotes (````backticks''``) to curly ones.

    .. seealso:: :func:`convert_backticks`
    """
    B = 1 << 2 | b
    """
    flag for double quotes (````backticks''``) and single quotes
    (```single'``) to curly ones.

    .. seealso:: :func:`convert_backticks` and :func:`convert_single_backticks`
    """
    mask_b = b | B

    d = 1 << 3
    """
    flag for dashes (``--``) to em-dashes.

    .. seealso:: :func:`convert_dashes`
    """
    D = 1 << 4 | d
    """
    flag for old-school typewriter dashes (``--``) to en-dashes and dashes
    (``---``) to em-dashes.

    .. seealso:: :func:`convert_dashes_oldschool`
    """
    i = 1 << 5 | d
    """
    flag for inverted old-school typewriter dashes (``--``) to em-dashes and
    dashes (``---``) to en-dashes.

    .. seealso:: :func:`convert_dashes_oldschool_inverted`
    """
    mask_d = d | D | i

    e = 1 << 6
    """
    flag for dashes (``...``) to ellipses.

    .. seealso:: :func:`convert_ellipses`
    """
    w = 1 << 7
    """
    flag for dashes (``&quot;``) to ASCII double quotes (``"``).

    This should be of no interest to most people, but of particular interest
    to anyone who writes their posts using Dreamweaver, as Dreamweaver
    inexplicably uses this entity to represent a literal double-quote
    character. SmartyPants only educates normal quotes, not entities (because
    ordinarily, entities are used for the explicit purpose of representing the
    specific character they represent). The "w" option must be used in
    conjunction with one (or both) of the other quote options ("q" or "b").
    Thus, if you wish to apply all SmartyPants transformations (quotes, en-
    and em-dashes, and ellipses) and also convert ``&quot;`` entities into
    regular quotes so SmartyPants can educate them.
    """

    u = 0 << 9 | 1 << 8
    """
    Output Unicode characters instead of numeric character references, for
    example, from ``&#8220;`` to left double quotation mark (``“``) (U+201C).

    .. seealso:: :func:`convert_entities`
    """
    h = 1 << 9 | 0 << 8
    """
    Output HTML named entities instead of numeric character references, for
    example, from ``&#8220;`` to ``&ldquo;``.

    .. seealso:: :func:`convert_entities`
    """
    s = 1 << 9 | 1 << 8
    """
    Output ASCII equivalents instead of numeric character references, for
    example, from ``&#8212;`` to ``--``.

    .. seealso:: :func:`convert_entities`
    """
    mask_o = u | h | s

    set0 = 0
    "suppress all transformations. (Do nothing.)"
    set1 = q | b | d | e
    "equivalent to :attr:`q` | :attr:`b` | :attr:`d` | :attr:`e`"
    set2 = q | b | D | e
    """
    equivalent to :attr:`q` | :attr:`b` | :attr:`D` | :attr:`e`

    For old school en- and em- dash.
    """
    set3 = q | b | i | e
    """
    equivalent to :attr:`q` | :attr:`b` | :attr:`i` | :attr:`e`

    For inverted old school en & em- dash."
    """
    @property
    def default(self):
        "Default value of attributes, same value as :attr:`set1`"
        global default_smartypants_attr
        return default_smartypants_attr

    @default.setter
    def default(self, attr):

        global default_smartypants_attr
        default_smartypants_attr = attr


Attr = _Attr()
"""
Processing attributes, which tells :func:`smartypants` what to convert

.. seealso:: :class:`_Attr`
"""
default_smartypants_attr = Attr.set1


tags_to_skip = ['pre', 'samp', 'code', 'tt', 'kbd', 'script', 'style', 'math']
"""
Skipped HTML elements

.. seealso:: :ref:`skip-html`
"""


def _tags_to_skip_regex(tags=None):
    """
    Convert a list of skipped tags into regular expression

    The default *tags* are :attr:`tags_to_skip`.

    >>> f = _tags_to_skip_regex
    >>> print(f(['foo', 'bar']).pattern)
    <(/)?(foo|bar)[^>]*>
    """
    if tags is None:
        tags = tags_to_skip

    if isinstance(tags, (list, tuple)):
        tags = '|'.join(tags)

    return re.compile('<(/)?(%s)[^>]*>' % tags, re.I)


def smartypants(text, attr=None):
    """
    SmartyPants function

    >>> print(smartypants('"foo" -- bar'))
    &#8220;foo&#8221; &#8212; bar
    >>> print(smartypants('"foo" -- bar', Attr.d))
    "foo" &#8212; bar
    """
    skipped_tag_stack = []

    if attr is None:
        attr = Attr.default

    do_quotes = attr & Attr.q
    do_backticks = attr & Attr.mask_b
    do_dashes = attr & Attr.mask_d
    do_ellipses = attr & Attr.e
    do_entities = attr & Attr.mask_o
    convert_quot = attr & Attr.w

    tokens = _tokenize(text)
    result = []
    in_pre = False

    prev_token_last_char = ""
    # This is a cheat, used to get some context
    # for one-character tokens that consist of
    # just a quote char. What we do is remember
    # the last character of the previous text
    # token, to use as context to curl single-
    # character quote tokens correctly.

    tags_to_skip_regex = _tags_to_skip_regex()

    for cur_token in tokens:
        if cur_token[0] == "tag":
            # Don't mess with quotes inside some tags.  This does not handle
            # self <closing/> tags!
            result.append(cur_token[1])
            skip_match = tags_to_skip_regex.match(cur_token[1])
            if skip_match:
                if not skip_match.group(1):
                    skipped_tag_stack.append(skip_match.group(2).lower())
                    in_pre = True
                else:
                    if len(skipped_tag_stack) > 0:
                        _tag = skipped_tag_stack[-1]
                        if skip_match.group(2).lower() == _tag:
                            skipped_tag_stack.pop()
                        else:
                            pass
                            # This close doesn't match the open.  This isn't
                            # XHTML.  We should barf here.
                    if len(skipped_tag_stack) == 0:
                        in_pre = False
        else:
            t = cur_token[1]
            # Remember last char of this token before processing.
            last_char = t[-1:]
            if not in_pre:
                t = process_escapes(t)

                if convert_quot:
                    t = re.sub('&quot;', '"', t)

                if do_dashes:
                    if do_dashes == Attr.d:
                        t = convert_dashes(t)
                    if do_dashes == Attr.D:
                        t = convert_dashes_oldschool(t)
                    if do_dashes == Attr.i:
                        t = convert_dashes_oldschool_inverted(t)

                if do_ellipses:
                    t = convert_ellipses(t)

                # Note: backticks need to be processed before quotes.
                if do_backticks == Attr.b:
                    t = convert_backticks(t)

                if do_backticks == Attr.B:
                    t = convert_single_backticks(t)

                if do_quotes:
                    if t == "'":
                        # Special case: single-character ' token
                        if re.match("\S", prev_token_last_char):
                            t = "&#8217;"
                        else:
                            t = "&#8216;"
                    elif t == '"':
                        # Special case: single-character " token
                        if re.match("\S", prev_token_last_char):
                            t = "&#8221;"
                        else:
                            t = "&#8220;"

                    else:
                        # Normal case:
                        t = convert_quotes(t)

                if do_entities:
                    mode = (0 if do_entities == Attr.u else
                            1 if do_entities == Attr.h else
                            2 if do_entities == Attr.s else
                            3)  # would result in key error
                    t = convert_entities(t, mode)

            prev_token_last_char = last_char
            result.append(t)

    return "".join(result)


def convert_quotes(text):
    """
    Convert quotes in *text* into HTML curly quote entities.

    >>> print(convert_quotes('"Isn\\'t this fun?"'))
    &#8220;Isn&#8217;t this fun?&#8221;
    """

    punct_class = r"""[!"#\$\%'()*+,-.\/:;<=>?\@\[\\\]\^_`{|}~]"""

    # Special case if the very first character is a quote
    # followed by punctuation at a non-word-break. Close the quotes by brute
    # force:
    text = re.sub(r"""^'(?=%s\\B)""" % (punct_class,), '&#8217;', text)
    text = re.sub(r"""^"(?=%s\\B)""" % (punct_class,), '&#8221;', text)

    # Special case for double sets of quotes, e.g.:
    #   <p>He said, "'Quoted' words in a larger quote."</p>
    text = re.sub(r""""'(?=\w)""", '&#8220;&#8216;', text)
    text = re.sub(r"""'"(?=\w)""", '&#8216;&#8220;', text)

    # Special case for decade abbreviations (the '80s):
    text = re.sub(r"""\b'(?=\d{2}s)""", '&#8217;', text)

    close_class = r'[^\ \t\r\n\[\{\(\-]'
    dec_dashes = '&#8211;|&#8212;'

    # Get most opening single quotes:
    opening_single_quotes_regex = re.compile(r"""
            (
                \s          |   # a whitespace char, or
                &nbsp;      |   # a non-breaking space entity, or
                --          |   # dashes, or
                &[mn]dash;  |   # named dash entities
                %s          |   # or decimal entities
                &\#x201[34];    # or hex
            )
            '                 # the quote
            (?=\w)            # followed by a word character
            """ % (dec_dashes,), re.VERBOSE)
    text = opening_single_quotes_regex.sub(r'\1&#8216;', text)

    closing_single_quotes_regex = re.compile(r"""
            (%s)
            '
            (?!\s | s\b | \d)
            """ % (close_class,), re.VERBOSE)
    text = closing_single_quotes_regex.sub(r'\1&#8217;', text)

    closing_single_quotes_regex = re.compile(r"""
            (%s)
            '
            (\s | s\b)
            """ % (close_class,), re.VERBOSE)
    text = closing_single_quotes_regex.sub(r'\1&#8217;\2', text)

    # Any remaining single quotes should be opening ones:
    text = re.sub("'", '&#8216;', text)

    # Get most opening double quotes:
    opening_double_quotes_regex = re.compile(r"""
            (
                \s          |   # a whitespace char, or
                &nbsp;      |   # a non-breaking space entity, or
                --          |   # dashes, or
                &[mn]dash;  |   # named dash entities
                %s          |   # or decimal entities
                &\#x201[34];    # or hex
            )
            "                 # the quote
            (?=\w)            # followed by a word character
            """ % (dec_dashes,), re.VERBOSE)
    text = opening_double_quotes_regex.sub(r'\1&#8220;', text)

    # Double closing quotes:
    closing_double_quotes_regex = re.compile(r"""
            #(%s)?   # character that indicates the quote should be closing
            "
            (?=\s)
            """ % (close_class,), re.VERBOSE)
    text = closing_double_quotes_regex.sub('&#8221;', text)

    closing_double_quotes_regex = re.compile(r"""
            (%s)   # character that indicates the quote should be closing
            "
            """ % (close_class,), re.VERBOSE)
    text = closing_double_quotes_regex.sub(r'\1&#8221;', text)

    # Any remaining quotes should be opening ones.
    text = re.sub('"', '&#8220;', text)

    return text


def convert_backticks(text):
    """
    Convert ````backticks''``-style double quotes in *text* into HTML curly
    quote entities.

    >>> print(convert_backticks("``Isn't this fun?''"))
    &#8220;Isn't this fun?&#8221;
    """

    text = re.sub('``', '&#8220;', text)
    text = re.sub("''", '&#8221;', text)
    return text


def convert_single_backticks(text):
    """
    Convert ```backticks'``-style single quotes in *text* into HTML curly
    quote entities.

    >>> print(convert_single_backticks("`Isn't this fun?'"))
    &#8216;Isn&#8217;t this fun?&#8217;
    """

    text = re.sub('`', '&#8216;', text)
    text = re.sub("'", '&#8217;', text)
    return text


def convert_dashes(text):
    """
    Convert ``--`` in *text* into em-dash HTML entities.

    >>> quote = 'Nothing endures but change. -- Heraclitus'
    >>> print(convert_dashes(quote))
    Nothing endures but change. &#8212; Heraclitus
    """

    text = re.sub('--', '&#8212;', text)
    return text


def convert_dashes_oldschool(text):
    """
    Convert ``--`` and ``---`` in *text* into en-dash and em-dash HTML
    entities, respectively.

    >>> quote = 'Life itself is the proper binge. --- Julia Child (1912--2004)'
    >>> print(convert_dashes_oldschool(quote))
    Life itself is the proper binge. &#8212; Julia Child (1912&#8211;2004)
    """

    text = re.sub('---', '&#8212;', text)  # em (yes, backwards)
    text = re.sub('--', '&#8211;', text)   # en (yes, backwards)
    return text


def convert_dashes_oldschool_inverted(text):
    """
    Convert ``--`` and ``---`` in *text* into em-dash and en-dash HTML
    entities, respectively.

    Two reasons why:

    * First, unlike the en- and em-dash syntax supported by
      :func:`convert_dashes_oldschool`, it's compatible with existing entries
      written before SmartyPants 1.1, back when ``--`` was only used for
      em-dashes.
    * Second, em-dashes are more common than en-dashes, and so it sort of
      makes sense that the shortcut should be shorter to type. (Thanks to Aaron
      Swartz for the idea.)

    >>> quote = 'Dare to be naïve. -- Buckminster Fuller (1895---1983)'
    >>> print(convert_dashes_oldschool_inverted(quote))
    Dare to be naïve. &#8212; Buckminster Fuller (1895&#8211;1983)
    """

    text = re.sub('---', '&#8211;', text)  # em
    text = re.sub('--', '&#8212;', text)   # en
    return text


def convert_ellipses(text):
    """
    Convert ``...`` in *text* into ellipsis HTML entities

    >>> print(convert_ellipses('Huh...?'))
    Huh&#8230;?
    """

    text = re.sub(r"""\.\.\.""", '&#8230;', text)
    text = re.sub(r"""\. \. \.""", '&#8230;', text)
    return text


def convert_entities(text, mode):
    """
    Convert numeric character references to, if *mode* is

    - *0*: Unicode characters
    - *1*: HTML named entities
    - *2*: ASCII equivalents

    >>> print(convert_entities('&#8216;', 0))
    ‘
    >>> print(convert_entities('&#8216;SmartyPants&#8217;', 1))
    &lsquo;SmartyPants&rsquo;
    >>> print(convert_entities('&#8220;Hello &#8212; world.&#8221;', 2))
    "Hello -- world."
    """

    CTBL = {
        '&#8211;': ('–', '&ndash;', '-'),
        '&#8212;': ('—', '&mdash;', '--'),
        '&#8216;': ('‘', '&lsquo;', "'"),
        '&#8217;': ('’', '&rsquo;', "'"),
        '&#8220;': ('“', '&ldquo;', '"'),
        '&#8221;': ('”', '&rdquo;', '"'),
        '&#8230;': ('…', '&hellip;', '...'),
    }

    for k, v in CTBL.items():
        text = text.replace(k, v[mode])

    return text


def process_escapes(text):
    r"""
    Processe the following backslash escape sequences in *text*. This is useful
    if you want to force a "dumb" quote or other character to appear.

    +--------+-----------+-----------+
    | Escape | Value     | Character |
    +========+===========+===========+
    | ``\\`` | ``&#92;`` | ``\``     |
    +--------+-----------+-----------+
    | ``\"`` | ``&#34;`` | ``"``     |
    +--------+-----------+-----------+
    | ``\'`` | ``&#39;`` | ``'``     |
    +--------+-----------+-----------+
    | ``\.`` | ``&#46;`` | ``.``     |
    +--------+-----------+-----------+
    | ``\-`` | ``&#45;`` | ``-``     |
    +--------+-----------+-----------+
    | ``\``` | ``&#96;`` | ``\```    |
    +--------+-----------+-----------+

    >>> print(process_escapes(r'\\'))
    &#92;
    >>> print(smartypants(r'"smarty" \"pants\"'))
    &#8220;smarty&#8221; &#34;pants&#34;
    """

    text = re.sub(r'\\\\', '&#92;', text)
    text = re.sub(r'\\"', '&#34;', text)
    text = re.sub(r"\\'", '&#39;', text)
    text = re.sub(r'\\\.', '&#46;', text)
    text = re.sub(r'\\-', '&#45;', text)
    text = re.sub(r'\\`', '&#96;', text)

    return text


def _tokenize(text):
    """
    Reference to an array of the tokens comprising the input string. Each token
    is either a tag (possibly with nested, tags contained therein, such as
    ``<a href="<MTFoo>">``, or a run of text between tags. Each element of the
    array is a two-element array; the first is either 'tag' or 'text'; the
    second is the actual value.

    Based on the _tokenize() subroutine from `Brad Choate's MTRegex plugin`__.

    __ http://www.bradchoate.com/past/mtregex.php
    """

    tokens = []

    tag_soup = re.compile(r'([^<]*)(<!--.*?--\s*>|<[^>]*>)', re.S)

    token_match = tag_soup.search(text)

    previous_end = 0
    while token_match:
        if token_match.group(1):
            tokens.append(['text', token_match.group(1)])

        # if -- in text part of comment, then it's not a comment, therefore it
        # should be converted.
        #
        # In HTML4 [1]:
        #   [...] Authors should avoid putting two or more adjacent hyphens
        #   inside comments.
        #
        # In HTML5 [2]:
        #   [...] the comment may have text, with the additional restriction
        #   that the text must not [...], nor contain two consecutive U+002D
        #   HYPHEN-MINUS characters (--)
        #
        # [1]: http://www.w3.org/TR/REC-html40/intro/sgmltut.html#h-3.2.4
        # [2]: http://www.w3.org/TR/html5/syntax.html#comments
        tag = token_match.group(2)
        type_ = 'tag'
        if tag.startswith('<!--'):
            # remove --[white space]> from the end of tag
            if '--' in tag[4:].rstrip('>').rstrip().rstrip('-'):
                type_ = 'text'
        tokens.append([type_, tag])

        previous_end = token_match.end()
        token_match = tag_soup.search(text, token_match.end())

    if previous_end < len(text):
        tokens.append(['text', text[previous_end:]])

    return tokens
