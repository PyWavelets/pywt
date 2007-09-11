#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Filip Wasilewski
# Date: $Date$

import docutils
import docutils.parsers.rst
import colorize

def code_block( name, arguments, options, content, lineno,
             content_offset, block_text, state, state_machine ):

    html = colorize.Parser('\n'.join(content).encode('utf-8')).format()
    raw = docutils.nodes.raw('', html, format = 'html')
    return [raw]

code_block.arguments = (1,0,0)
code_block.options = {'language' : docutils.parsers.rst.directives.unchanged }
code_block.content = 1
  
docutils.parsers.rst.directives.register_directive('code-block', code_block )

def publish():
    import docutils.core
    docutils.core.publish_cmdline(writer_name='html')

if __name__ == "__main__":
    publish()
