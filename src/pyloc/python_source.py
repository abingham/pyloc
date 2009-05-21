from ply.lex import TOKEN
import re

class LOCLexer(object):
    '''count loc in python

     * total: all lines of all sorts
     * code: lines that have any sort of actual code
     * comment: lines that have any sort of commentary. This includes
       docstring lines (see below)
     * blank: lines that are completely empty
     * docstring: lines that look like docstrings (though we don't
       enough parsing to determine if they're actually docstrings)
    '''
    tokens = ( 'COMMENT_LINE',
               'MULTILINE_SINGLE_STRING',
               'MULTILINE_DOUBLE_STRING',
               'SINGLE_STRING',
               'DOUBLE_STRING',
               )

    space = r'[ \t\r\f\v]*'
    escaped_quote = r'(\\\')*'
    escaped_double_quote = r'(\\\")*'

    def t_COMMENT_LINE(self, t):
        r'\#.*'
        if not self.comment_line:
            self.comment_line_count += 1
            self.comment_line = True
        self.empty_line = False

    def multiline_string(self, t):
        lines = len(t.value.split('\n'))

        if self.empty_line:
            self.docstring_line_count += lines
            self.comment_line_count += lines
            self.comment_line = True

        self.empty_line = False
        self.lexer.lineno += lines - 1

    @TOKEN(r"'''(.|\n)*?" + escaped_quote + r"'''")
    def t_MULTILINE_SINGLE_STRING(self, t):
        self.multiline_string(t)

    @TOKEN(r'"""(.|\n)*?' + escaped_double_quote + '"""')
    def t_MULTILINE_DOUBLE_STRING(self, t):
        self.multiline_string(t)

    def singleline_string(self, t):
        if self.empty_line:
            self.docstring_line_count += 1
            self.comment_line_count += 1
            self.comment_line = True
        self.empty_line = False        

    @TOKEN(r"'(.|\\\')*'")
    def t_SINGLE_STRING(self, t):
        self.singleline_string(t)

    @TOKEN(r'"(.|\\\")*"')
    def t_DOUBLE_STRING(self, t):
        self.singleline_string(t)

    def t_CODE(self, t):
        r'\S(^\#)*'
        if not self.code_line:
            self.code_line = True
            self.code_line_count += 1
        self.empty_line = False

    @TOKEN(r'\n')
    def t_newline(self, t):
        if self.empty_line:
            self.empty_line_count += 1
        self.lexer.lineno += 1
        self.empty_line = True
        self.comment_line = False
        self.code_line = False

    space_re = re.compile(space)
    def t_error(self, t):
        # self.empty_line = False
        t.lexer.skip(1) 

    def line_count(self):
        return self.lexer.lineno - 1

    def build(self, **kwargs):
        import ply.lex
        self.lexer = ply.lex.lex(object=self,**kwargs)

    def __init__(self):
        self.code_line_count = 0
        self.code_line = False

        self.empty_line_count = 0
        self.empty_line = True

        self.comment_line_count = 0
        self.comment_line = False

        self.docstring_line_count = 0

def loc(f):
    '''count lines of code in python files

    :param f: a file-like object from which to read the code
    '''

    l = LOCLexer()
    l.build()
    l.lexer.input(f.read())
    while True:
        tok = l.lexer.token()
        if not tok: break

    return { 'total' : l.line_count(),
             'code' : l.code_line_count,
             'empty' : l.empty_line_count,
             'comment' : l.comment_line_count,
             'docstring' : l.docstring_line_count }

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
    print 'code:',     l.code_line_count
    print 'empty:',    l.empty_line_count
    print 'comment:',  l.comment_line_count
    print 'docstring:',l.docstring_line_count
