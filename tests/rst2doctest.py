#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Filip Wasilewski
# Date: $Date: 2006-07-05 16:19:42 +0200 (Śr, 05 lip 2006) $

"""
Extracts code-blocks from reStructuredText and produces Python doctests.
(I hate when examples from documentation does not work)

Usage: rst2doctest.py input.rst > test_doc.py
"""

import sys, os.path

import docutils.writers
import docutils.parsers.rst
from docutils.core import publish_cmdline, publish_programmatically

if len(sys.argv) != 2:
    print "Usage: %s input.rst > test_doc.py" % os.path.basename(sys.argv[0])
    raise SystemExit
    
input = sys.argv[1]

class NullWriter(docutils.writers.Writer):
    def translate(self):
        pass
    def write(self, document, destination):
        pass

doctest = []
codeblock_no = 1

def code_block( name, arguments, options, content, lineno,
             content_offset, block_text, state, state_machine ):

    """
    Creates Python doctests from code-blocks

    .. code-block:: Python
      
      >>> print 1+2
      >>> 3
    """

    global doctest, codeblock_no
    doctest.append('\n')
    doctest.append('def test_%d_on_line_%d():\n' % (codeblock_no, lineno))
    codeblock_no += 1
    
    doctest.append('    """\n')
    for line in content:
        doctest.append('    ' + line + '\n')
    doctest.append('    """\n')
    doctest.append('\n')

    #raw = docutils.nodes.doctest_block(content,'\n'.join(content))
    #return [raw]

code_block.arguments = (1,0,0)
code_block.options = {'language' : docutils.parsers.rst.directives.unchanged }
code_block.content = 1
  
docutils.parsers.rst.directives.register_directive('code-block', code_block )

publish_programmatically(source_class=docutils.io.FileInput, source=None,
    source_path=input, destination_class=docutils.io.FileOutput, destination=None,
    destination_path=None, reader=None, reader_name='standalone',
    parser=None, parser_name='restructuredtext', writer=NullWriter(),
    writer_name=None, settings=None, settings_spec=None,
    settings_overrides=None, config_section=None, enable_exit_status=None)

f = sys.stdout

doctest_head = """#!/usr/bin/env python\n\n# Doctest for %s document\n"""

doctest_stub = """
def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
"""

f.write(doctest_head % input)
f.writelines(doctest)
f.write(doctest_stub)
f.close()
