from ply.lex import TOKEN

class LOCLexer:
    tokens = ( 'COMMENT_LINE',
               'MULTILINE_SINGLE_STRING',
               'MULTILINE_DOUBLE_STRING',
               'SINGLE_STRING',
               'DOUBLE_STRING',
               )

    space = r'[\t\ ]*'
    escaped_quote = r'(\\\')*'
    escaped_double_quote = r'(\\\")*'

    @TOKEN(space + r'\#')
    def t_COMMENT_LINE(self, t):
        if self.empty_line:
            self.comment_line_count += 1
        self.empty_line = False

    @TOKEN(space + r"'''(.|\n)*?" + escaped_quote + "'''")
    def t_MULTILINE_SINGLE_STRING(self, t):
        lines = len(t.value.split('\n'))
        if self.empty_line:
            self.docstring_line_count += lines

        self.empty_line = False
        self.lexer.lineno += lines - 1

    @TOKEN(space + r'"""(.|\n)*?' + escaped_double_quote + '"""')
    def t_MULTILINE_DOUBLE_STRING(self, t):
        lines = len(t.value.split('\n'))
        if self.empty_line:
            self.docstring_line_count += lines

        self.empty_line = False
        self.lexer.lineno += lines - 1

    @TOKEN(space + r"'(.|\\\')*'")
    def t_SINGLE_STRING(self, t):
        if self.empty_line:
            self.docstring_line_count += 1
        self.empty_line = False

    @TOKEN(space + r'"(.|\\\")*"')
    def t_DOUBLE_STRING(self, t):
        if self.empty_line:
            self.docstring_line_count += 1
        self.empty_line = False

    @TOKEN(space + r'\n')
    def t_newline(self, t):
        if self.empty_line:
            self.empty_line_count += 1
        self.lexer.lineno += 1
        self.empty_line = True

    def t_error(self, t):
        self.empty_line = False
        t.lexer.skip(1) 

    def line_count(self):
        return self.lexer.lineno - 1

    def build(self, **kwargs):
        import ply.lex
        self.lexer = ply.lex.lex(object=self,**kwargs)

    def __init__(self, **kwargs):
        self.empty_line_count = 0
        self.empty_line = True

        self.comment_line_count = 0

        self.quote_type = None
        self.docstring_line_count = 0

import cStringIO

def loc(filename):
    '''count lines of code in python files'''

    l = LOCLexer()
    l.build()
    io = cStringIO.StringIO()
    io.write(open(filename, 'r').read())
    l.lexer.input(io.getvalue())
    while True:
        tok = l.lexer.token()
        if not tok: break

    return { 'total' : l.line_count(),
             'minimum' : l.line_count() - l.empty_line_count - l.comment_line_count - l.docstring_line_count,
             'empty' : l.empty_line_count,
             'comment' : l.comment_line_count,
             'docstring' : l.docstring_line_count }
    return l.line_count() - l.empty_line_count, l.line_count()

if __name__ == '__main__':
    '''a simple spot-test harness'''
    l = LOCLexer()
    l.build()

    import cStringIO
    io = cStringIO.StringIO()
    io.write(open('test_data.py', 'r').read())
    l.lexer.input(io.getvalue())
    while True:
        tok = l.lexer.token()
        if not tok: break
        
    print io.getvalue()
    print 'total:',    l.line_count()
    print 'empty:',    l.empty_line_count
    print 'comment:',  l.comment_line_count
    print 'docstring:',l.docstring_line_count
