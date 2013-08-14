#!/usr/bin/python
# Copyright (c) 2013 Yu-Jie Lin
# Copyright (c) 2004, 2005, 2007, 2013 Chad Miller
# Copyright (c) 2003 John Gruber
# Licensed under the BSD License, for detailed license information, see COPYING

__author__ = 'Yu-Jie Lin'
__author_email__ = 'livibetter@gmail.com'
__version__ = '1.7.1'
__license__ = 'BSD License'
__url__ = 'https://bitbucket.org/livibetter/smartypants.py'
__description__ = 'Python with the SmartyPants'

default_smartypants_attr = "1"

import re
import warnings

tags_to_skip_regex = re.compile('<(/)?(pre|code|kbd|script|math)[^>]*>', re.I)


def verify_installation(request):

    msg = 'Pyblosxom support will be removed at Version 2.0.0'
    warnings.filterwarnings('once', msg, DeprecationWarning)
    warnings.warn(msg, DeprecationWarning)
    return 1
    # assert the plugin is functional


def cb_story(args):

    msg = 'Pyblosxom support will be removed at Version 2.0.0'
    warnings.filterwarnings('once', msg, DeprecationWarning)
    warnings.warn(msg, DeprecationWarning)

    global default_smartypants_attr

    try:
        forbidden_flavours = args["entry"]["smartypants_forbidden_flavours"]
    except KeyError:
        forbidden_flavours = ["rss"]

    try:
        attributes = args["entry"]["smartypants_attributes"]
    except KeyError:
        attributes = default_smartypants_attr

    if attributes is None:
        attributes = default_smartypants_attr

    entryData = args["entry"].getData()

    try:
        if args["request"]["flavour"] in forbidden_flavours:
            return
    except KeyError:
        if "&lt;" in args["entry"]["body"][0:15]:  # sniff the stream
            return  # abort if it looks like escaped HTML.  FIXME

    # FIXME: make these configurable, perhaps?
    args["entry"]["body"] = smartyPants(entryData, attributes)
    args["entry"]["title"] = smartyPants(args["entry"]["title"], attributes)


### interal functions below here

def smartyPants(text, attr=default_smartypants_attr):
    # should we translate &quot; entities into normal quotes?
    convert_quot = 0

    # Parse attributes:
    # 0 : do nothing
    # 1 : set all
    # 2 : set all, using old school en- and em- dash shortcuts
    # 3 : set all, using inverted old school en and em- dash shortcuts
    #
    # q : quotes
    # b : backtick quotes (``double'' only)
    # B : backtick quotes (``double'' and `single')
    # d : dashes
    # D : old school dashes
    # i : inverted old school dashes
    # e : ellipses
    # w : convert &quot; entities to " for Dreamweaver users

    skipped_tag_stack = []
    do_dashes = 0
    do_backticks = 0
    do_quotes = 0
    do_ellipses = 0
    do_stupefy = 0

    if attr == "0":
        # Do nothing.
        return text
    elif attr == "1":
        do_quotes = 1
        do_backticks = 1
        do_dashes = 1
        do_ellipses = 1
    elif attr == "2":
        # Do everything, turn all options on, use old school dash shorthand.
        do_quotes = 1
        do_backticks = 1
        do_dashes = 2
        do_ellipses = 1
    elif attr == "3":
        # Do everything, turn all options on, use inverted old school dash
        # shorthand.
        do_quotes = 1
        do_backticks = 1
        do_dashes = 3
        do_ellipses = 1
    elif attr == "-1":
        # Special "stupefy" mode.
        do_stupefy = 1
    else:
        for c in attr:
            if c == "q":
                do_quotes = 1
            elif c == "b":
                do_backticks = 1
            elif c == "B":
                do_backticks = 2
            elif c == "d":
                do_dashes = 1
            elif c == "D":
                do_dashes = 2
            elif c == "i":
                do_dashes = 3
            elif c == "e":
                do_ellipses = 1
            elif c == "w":
                convert_quot = 1
            else:
                pass
                # ignore unknown option

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
                t = processEscapes(t)

                if convert_quot:
                    t = re.sub('&quot;', '"', t)

                if do_dashes:
                    if do_dashes == 1:
                        t = educateDashes(t)
                    if do_dashes == 2:
                        t = educateDashesOldSchool(t)
                    if do_dashes == 3:
                        t = educateDashesOldSchoolInverted(t)

                if do_ellipses:
                    t = educateEllipses(t)

                # Note: backticks need to be processed before quotes.
                if do_backticks:
                    t = educateBackticks(t)

                if do_backticks == 2:
                    t = educateSingleBackticks(t)

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
                        t = educateQuotes(t)

                if do_stupefy == 1:
                    t = stupefyEntities(t)

            prev_token_last_char = last_char
            result.append(t)

    return "".join(result)


def educateQuotes(text):
    """
    Parameter:  String.

    Returns:    The string, with "educated" curly quote HTML entities.

    >>> print(educateQuotes('"Isn\\'t this fun?"'))
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


def educateBackticks(text):
    """
    Parameter:  String.
    Returns:    The string, with ``backticks'' -style double quotes
                translated into HTML curly quote entities.

    >>> print(educateBackticks("``Isn't this fun?''"))
    &#8220;Isn't this fun?&#8221;
    """

    text = re.sub('``', '&#8220;', text)
    text = re.sub("''", '&#8221;', text)
    return text


def educateSingleBackticks(text):
    """
    Parameter:  String.
    Returns:    The string, with `backticks' -style single quotes
                translated into HTML curly quote entities.

    >>> print(educateSingleBackticks("`Isn't this fun?'"))
    &#8216;Isn&#8217;t this fun?&#8217;
    """

    text = re.sub('`', '&#8216;', text)
    text = re.sub("'", '&#8217;', text)
    return text


def educateDashes(text):
    """
    Parameter:  String.

    Returns:    The string, with each instance of "--" translated to
                an em-dash HTML entity.
    """

    text = re.sub('---', '&#8211;', text)  # en  (yes, backwards)
    text = re.sub('--', '&#8212;', text)   # em (yes, backwards)
    return text


def educateDashesOldSchool(text):
    """
    Parameter:  String.

    Returns:    The string, with each instance of "--" translated to
                an en-dash HTML entity, and each "---" translated to
                an em-dash HTML entity.
    """

    text = re.sub('---', '&#8212;', text)    # em (yes, backwards)
    text = re.sub('--', '&#8211;', text)    # en (yes, backwards)
    return text


def educateDashesOldSchoolInverted(text):
    """
    Parameter:  String.

    Returns:    The string, with each instance of "--" translated to
                an em-dash HTML entity, and each "---" translated to
                an en-dash HTML entity. Two reasons why: First, unlike the
                en- and em-dash syntax supported by
                EducateDashesOldSchool(), it's compatible with existing
                entries written before SmartyPants 1.1, back when "--" was
                only used for em-dashes.  Second, em-dashes are more
                common than en-dashes, and so it sort of makes sense that
                the shortcut should be shorter to type. (Thanks to Aaron
                Swartz for the idea.)
    """

    text = re.sub('---', '&#8211;', text)    # em
    text = re.sub('--', '&#8212;', text)    # en
    return text


def educateEllipses(text):
    """
    Parameter:  String.
    Returns:    The string, with each instance of "..." translated to
                an ellipsis HTML entity.

    >>> print(educateEllipses('Huh...?'))
    Huh&#8230;?
    """

    text = re.sub(r"""\.\.\.""", '&#8230;', text)
    text = re.sub(r"""\. \. \.""", '&#8230;', text)
    return text


def stupefyEntities(text):
    """
    Parameter:  String.
    Returns:    The string, with each SmartyPants HTML entity translated to
                its ASCII counterpart.

    >>> print(stupefyEntities('&#8220;Hello &#8212; world.&#8221;'))
    "Hello -- world."
    """

    text = re.sub('&#8211;', '-', text)  # en-dash
    text = re.sub('&#8212;', '--', text)  # em-dash

    text = re.sub('&#8216;', "'", text)  # open single quote
    text = re.sub('&#8217;', "'", text)  # close single quote

    text = re.sub('&#8220;', '"', text)  # open double quote
    text = re.sub('&#8221;', '"', text)  # close double quote

    text = re.sub('&#8230;', '...', text)  # ellipsis

    return text


def processEscapes(text):
    r"""
    Parameter:  String.
    Returns:    The string, with after processing the following backslash
                escape sequences. This is useful if you want to force a "dumb"
                quote or other character to appear.

                Escape  Value
                ------  -----
                \\      &#92;
                \"      &#34;
                \'      &#39;
                \.      &#46;
                \-      &#45;
                \`      &#96;
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
    Parameter:  String containing HTML markup.
    Returns:    Reference to an array of the tokens comprising the input
                string. Each token is either a tag (possibly with nested,
                tags contained therein, such as <a href="<MTFoo>">, or a
                run of text between tags. Each element of the array is a
                two-element array; the first is either 'tag' or 'text';
                the second is the actual value.

    Based on the _tokenize() subroutine from Brad Choate's MTRegex plugin.
        <http://www.bradchoate.com/past/mtregex.php>
    """

    tokens = []

    tag_soup = re.compile('([^<]*)(<[^>]*>)')

    token_match = tag_soup.search(text)

    previous_end = 0
    while token_match:
        if token_match.group(1):
            tokens.append(['text', token_match.group(1)])

        tokens.append(['tag', token_match.group(2)])

        previous_end = token_match.end()
        token_match = tag_soup.search(text, token_match.end())

    if previous_end < len(text):
        tokens.append(['text', text[previous_end:]])

    return tokens
