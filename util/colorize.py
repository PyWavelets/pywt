#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgi, string, sys, cStringIO
import keyword, token, tokenize


_KEYWORD = token.NT_OFFSET + 1
_TEXT    = token.NT_OFFSET + 2
_PROMPT  = token.NT_OFFSET + 3
_WHITESPACE  = token.NT_OFFSET + 3
    
import token, tokenize

class TokenFormatter(object):
    def __init__(self):
        self.css = {
            token.NUMBER:          'num',
            tokenize.OP:           'op',
            token.STRING:          'str',
            tokenize.COMMENT:      'com',
            tokenize.NAME:         'name',
            tokenize.ERRORTOKEN:   'err',
            _KEYWORD:              'kwd',
            _TEXT:                 'txt',
            _PROMPT:               'pmt',
        }
        
        self.indent_level = 0
        self.indent_text = "&nbsp" * 4
        self.prompt_text = '>>>'
        
    def new_line(self):
        return "<br />" + self.indent_level * self.indent_text
    
    def classify(self, toktype, toktext):
        if toktype in self.css:
            s = '<span class="%s">%s</span>' % (self.css[toktype], cgi.escape(toktext).replace(' ', '&nbsp'))
        else:
            s = ''
        return s
        
    def __call__(self, toktype, toktext, (srow,scol), (erow,ecol), line):
        if toktype == tokenize.INDENT:
            self.indent_level += 1
            return self.indent_text
        elif toktype == tokenize.DEDENT:
            self.indent_level -= 1
            return ''
        elif toktype == _WHITESPACE:
            return toktext.replace(' ', '&nbsp')
        elif toktype in (tokenize.NEWLINE, tokenize.NL):
            return self.new_line()
        else:
            if token.LPAR <= toktype and toktype <= token.OP:
                toktype = token.OP
                if srow == 0 and toktext == self.prompt_text:
                    toktype = _PROMPT
            elif toktype == token.NAME and keyword.iskeyword(toktext):
                toktype = _KEYWORD
            return self.classify(toktype, toktext)
               
            
class Parser(object):
    """ Send colored python source.
    """

    def __init__(self, raw):
        """ Store the source text.
        """
        self.raw = raw.strip().expandtabs()
        self.format_token = TokenFormatter()
        self.out = cStringIO.StringIO()
        
    def format(self):
        input = cStringIO.StringIO(self.raw)
        self.pos = 0

        self.lines = [0, 0]
        pos = 0
        while True:
            try:
                pos = self.raw.index('\n', pos) + 1
            except ValueError:
                break
            self.lines.append(pos)
        self.lines.append(len(self.raw)) 

        self.out.write('<div class="code">')
        try:
            tokenize.tokenize(input.readline, self)
        except tokenize.TokenError, ex:
            msg = ex[0]
            line = ex[1][0]
            self.out.write("<h3>ERROR: %s</h3>%s\n" % (msg, line))
        self.out.write('\n</div>')
        return self.out.getvalue()
 
    def __call__(self, toktype, toktext, (srow,scol), (erow,ecol), line):
        """ Token handler.
        """
        if 0:
            print "type", toktype, token.tok_name[toktype], "text", toktext,
            print "start", srow,scol, "end", erow,ecol

        oldpos = self.pos
        newpos = self.lines[srow] + scol
        self.pos = newpos + len(toktext) 
        
        if newpos > oldpos:
            self.out.write(self.format_token(_WHITESPACE, self.raw[oldpos:newpos], (srow,scol), (erow,ecol), line)) 

        self.out.write(self.format_token(toktype, toktext, (srow,scol), (erow,ecol), line))


