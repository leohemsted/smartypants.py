#!/usr/bin/python
# Copyright (c) 2013 Yu-Jie Lin
# Copyright (c) 2004, 2005, 2007, 2013 Chad Miller
# Copyright (c) 2003 John Gruber
# For detail license information, See COPYING

__author__ = 'Yu-Jie Lin'
__email__ = 'livibetter@gmail.com'
__version__ = '1.7.0dev'
__license__ = 'BSD License'
__url__ = 'https://bitbucket.org/livibetter/smartypants.py'
__description__ = 'Smart-quotes, smart-ellipses, and smart-dashes'

default_smartypants_attr = "1"

import re

tags_to_skip_regex = re.compile(r"<(/)?(pre|code|kbd|script|math)[^>]*>", re.I)


def verify_installation(request):
    return 1
    # assert the plugin is functional


def cb_story(args):
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
    convert_quot = False

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
    do_dashes = "0"
    do_backticks = "0"
    do_quotes = "0"
    do_ellipses = "0"
    do_stupefy = "0"

    if attr == "0":
        # Do nothing.
        return text
    elif attr == "1":
        do_quotes = "1"
        do_backticks = "1"
        do_dashes = "1"
        do_ellipses = "1"
    elif attr == "2":
        # Do everything, turn all options on, use old school dash shorthand.
        do_quotes = "1"
        do_backticks = "1"
        do_dashes = "2"
        do_ellipses = "1"
    elif attr == "3":
        # Do everything, turn all options on, use inverted old school dash
        # shorthand.
        do_quotes = "1"
        do_backticks = "1"
        do_dashes = "3"
        do_ellipses = "1"
    elif attr == "-1":
        # Special "stupefy" mode.
        do_stupefy = "1"
    else:
        for c in attr:
            if c == "q":
                do_quotes = "1"
            elif c == "b":
                do_backticks = "1"
            elif c == "B":
                do_backticks = "2"
            elif c == "d":
                do_dashes = "1"
            elif c == "D":
                do_dashes = "2"
            elif c == "i":
                do_dashes = "3"
            elif c == "e":
                do_ellipses = "1"
            elif c == "w":
                convert_quot = "1"
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
            if skip_match is not None:
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

                if convert_quot != "0":
                    t = re.sub('&quot;', '"', t)

                if do_dashes != "0":
                    if do_dashes == "1":
                        t = educateDashes(t)
                    if do_dashes == "2":
                        t = educateDashesOldSchool(t)
                    if do_dashes == "3":
                        t = educateDashesOldSchoolInverted(t)

                if do_ellipses != "0":
                    t = educateEllipses(t)

                # Note: backticks need to be processed before quotes.
                if do_backticks != "0":
                    t = educateBackticks(t)

                if do_backticks == "2":
                    t = educateSingleBackticks(t)

                if do_quotes != "0":
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

                if do_stupefy == "1":
                    t = stupefyEntities(t)

            prev_token_last_char = last_char
            result.append(t)

    return "".join(result)


def educateQuotes(str):
    """
    Parameter:  String.

    Returns:    The string, with "educated" curly quote HTML entities.

    Example input:  "Isn't this fun?"
    Example output: &#8220;Isn&#8217;t this fun?&#8221;
    """

    punct_class = r"""[!"#\$\%'()*+,-.\/:;<=>?\@\[\\\]\^_`{|}~]"""

    # Special case if the very first character is a quote
    # followed by punctuation at a non-word-break. Close the quotes by brute
    # force:
    str = re.sub(r"""^'(?=%s\\B)""" % (punct_class,), r"""&#8217;""", str)
    str = re.sub(r"""^"(?=%s\\B)""" % (punct_class,), r"""&#8221;""", str)

    # Special case for double sets of quotes, e.g.:
    #   <p>He said, "'Quoted' words in a larger quote."</p>
    str = re.sub(r""""'(?=\w)""", """&#8220;&#8216;""", str)
    str = re.sub(r"""'"(?=\w)""", """&#8216;&#8220;""", str)

    # Special case for decade abbreviations (the '80s):
    str = re.sub(r"""\b'(?=\d{2}s)""", r"""&#8217;""", str)

    close_class = r"""[^\ \t\r\n\[\{\(\-]"""
    dec_dashes = r"""&#8211;|&#8212;"""

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
    str = opening_single_quotes_regex.sub(r"""\1&#8216;""", str)

    closing_single_quotes_regex = re.compile(r"""
            (%s)
            '
            (?!\s | s\b | \d)
            """ % (close_class,), re.VERBOSE)
    str = closing_single_quotes_regex.sub(r"""\1&#8217;""", str)

    closing_single_quotes_regex = re.compile(r"""
            (%s)
            '
            (\s | s\b)
            """ % (close_class,), re.VERBOSE)
    str = closing_single_quotes_regex.sub(r"""\1&#8217;\2""", str)

    # Any remaining single quotes should be opening ones:
    str = re.sub(r"""'""", r"""&#8216;""", str)

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
    str = opening_double_quotes_regex.sub(r"""\1&#8220;""", str)

    # Double closing quotes:
    closing_double_quotes_regex = re.compile(r"""
            #(%s)?   # character that indicates the quote should be closing
            "
            (?=\s)
            """ % (close_class,), re.VERBOSE)
    str = closing_double_quotes_regex.sub(r"""&#8221;""", str)

    closing_double_quotes_regex = re.compile(r"""
            (%s)   # character that indicates the quote should be closing
            "
            """ % (close_class,), re.VERBOSE)
    str = closing_double_quotes_regex.sub(r"""\1&#8221;""", str)

    # Any remaining quotes should be opening ones.
    str = re.sub(r'"', r"""&#8220;""", str)

    return str


def educateBackticks(str):
    """
    Parameter:  String.
    Returns:    The string, with ``backticks'' -style double quotes
                translated into HTML curly quote entities.
    Example input:  ``Isn't this fun?''
    Example output: &#8220;Isn't this fun?&#8221;
    """

    str = re.sub(r"""``""", r"""&#8220;""", str)
    str = re.sub(r"""''""", r"""&#8221;""", str)
    return str


def educateSingleBackticks(str):
    """
    Parameter:  String.
    Returns:    The string, with `backticks' -style single quotes
                translated into HTML curly quote entities.

    Example input:  `Isn't this fun?'
    Example output: &#8216;Isn&#8217;t this fun?&#8217;
    """

    str = re.sub(r"""`""", r"""&#8216;""", str)
    str = re.sub(r"""'""", r"""&#8217;""", str)
    return str


def educateDashes(str):
    """
    Parameter:  String.

    Returns:    The string, with each instance of "--" translated to
                an em-dash HTML entity.
    """

    str = re.sub(r"""---""", r"""&#8211;""", str)  # en  (yes, backwards)
    str = re.sub(r"""--""", r"""&#8212;""", str)   # em (yes, backwards)
    return str


def educateDashesOldSchool(str):
    """
    Parameter:  String.

    Returns:    The string, with each instance of "--" translated to
                an en-dash HTML entity, and each "---" translated to
                an em-dash HTML entity.
    """

    str = re.sub(r"""---""", r"""&#8212;""", str)    # em (yes, backwards)
    str = re.sub(r"""--""", r"""&#8211;""", str)    # en (yes, backwards)
    return str


def educateDashesOldSchoolInverted(str):
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
    str = re.sub(r"""---""", r"""&#8211;""", str)    # em
    str = re.sub(r"""--""", r"""&#8212;""", str)    # en
    return str


def educateEllipses(str):
    """
    Parameter:  String.
    Returns:    The string, with each instance of "..." translated to
                an ellipsis HTML entity.

    Example input:  Huh...?
    Example output: Huh&#8230;?
    """

    str = re.sub(r"""\.\.\.""", r"""&#8230;""", str)
    str = re.sub(r"""\. \. \.""", r"""&#8230;""", str)
    return str


def stupefyEntities(str):
    """
    Parameter:  String.
    Returns:    The string, with each SmartyPants HTML entity translated to
                its ASCII counterpart.

    Example input:  &#8220;Hello &#8212; world.&#8221;
    Example output: "Hello -- world."
    """

    str = re.sub(r"""&#8211;""", r"""-""", str)  # en-dash
    str = re.sub(r"""&#8212;""", r"""--""", str)  # em-dash

    str = re.sub(r"""&#8216;""", r"""'""", str)  # open single quote
    str = re.sub(r"""&#8217;""", r"""'""", str)  # close single quote

    str = re.sub(r"""&#8220;""", r'''"''', str)  # open double quote
    str = re.sub(r"""&#8221;""", r'''"''', str)  # close double quote

    str = re.sub(r"""&#8230;""", r"""...""", str)  # ellipsis

    return str


def processEscapes(str):
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
    str = re.sub(r"""\\\\""", r"""&#92;""", str)
    str = re.sub(r'''\\"''', r"""&#34;""", str)
    str = re.sub(r"""\\'""", r"""&#39;""", str)
    str = re.sub(r"""\\\.""", r"""&#46;""", str)
    str = re.sub(r"""\\-""", r"""&#45;""", str)
    str = re.sub(r"""\\`""", r"""&#96;""", str)

    return str


def _tokenize(str):
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

    tag_soup = re.compile(r"""([^<]*)(<[^>]*>)""")

    token_match = tag_soup.search(str)

    previous_end = 0
    while token_match is not None:
        if token_match.group(1):
            tokens.append(['text', token_match.group(1)])

        tokens.append(['tag', token_match.group(2)])

        previous_end = token_match.end()
        token_match = tag_soup.search(str, token_match.end())

    if previous_end < len(str):
        tokens.append(['text', str[previous_end:]])

    return tokens
