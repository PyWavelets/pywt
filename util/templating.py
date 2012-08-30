#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Filip Wasilewski
# Date: $Date$

# Ok, not really a full-featured templating language, but good enough
# to keep the code easier to maintain.
# PS. For internal use only ;)

import glob
import os
import re

pattern_for = re.compile(r"""(?P<for>
                                ^\s*
                                    (?:/{2,})?  # optional C comment
                                    \s*
                                    \#{2}       # two hashes
                                    \s*

                                    (FOR)
                                        \s+ (?P<variable>[\w$][\d\w$]*) \s+
                                    (IN)
                                        \s+ \(
                                        (?P<values>
                                            (?:
                                                \s* [^,\s]+ , \s*
                                            )+
                                            (?:
                                                [^,\s]+
                                            ){0,1}
                                            \s*
                                        )
                                        \)
                                    \s* : \s*
                             )
                             ^(?P<body>.*?)
                             (?P<endfor>
                                ^
                                    \s*
                                    (?:/{2,})?  # optional C comment
                                    \s*
                                    \#{2}       # two hashes
                                    \s*
                                    (ENDFOR)
                                        \s+ (?P=variable) \s*?\n
                             )
""", re.X | re.M | re.S | re.I)


def expand_template(s):
    """
    Currently it only does a simple repeat-and-replace in a loop:

    FOR $variable$ IN (value1, value2, ...):
        ... start block ...
        $variable$
        ... end block ...
    ENDFOR $variable$

    The above will repeat the block for every value from the list each time
    substituting the $variable$ with the current value.

        >>> s = \
        ... '''
        ... w = 9
        ... ## FOR $x$ IN (7, w):
        ...   ## FOR $y$ IN ("{", 1):
        ... print $x$, $y$, "$x$_$y$"
        ...   ## ENDFOR $y$
        ... ## ENDFOR $x$'''
        >>> print expand_template(s)

        w = 9
        print 7, "{"
        print 7, 1
        print w, "{"
        print w, 1
    """
    while True:
        m = pattern_for.search(s)
        if not m:
            break

        new_body = ''
        for value in [
            v.strip() for v in m.group('values').split(',') if v.strip()
        ]:
            new_body += m.group('body').replace(m.group('variable'), value)

        s = s[:m.start()] + new_body + s[m.end():]

    return s


def get_destination_filepath(source):
    root, template_name = os.path.split(source)

    # main extension
    destination_name, base_ext = os.path.splitext(template_name)

    while os.path.extsep in destination_name:
        # remove .template extension for files like file.template.c
        destination_name = os.path.splitext(destination_name)[0]
    return os.path.join(root, destination_name + base_ext)


def needs_update(template_path, destination_path):
    if not os.path.exists(destination_path):
        return True
    if os.path.getmtime(destination_path) < os.path.getmtime(template_path):
        return True
    return False


def expand_files(glob_pattern, force_update=False):
    files = glob.glob(glob_pattern)
    for template_path in files:
        destination_path = get_destination_filepath(template_path)
        if force_update or needs_update(template_path, destination_path):
            print "expanding template: %s -> %s" % (
                template_path, destination_path)
            content = expand_template(open(template_path, "rb").read())
            new_file = open(destination_path, "wb")
            new_file.write(content)
            new_file.close()
