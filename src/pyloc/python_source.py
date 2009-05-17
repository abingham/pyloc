from ply.lex import TOKEN

class LOCLexer:
    tokens = ( 'COMMENT_LINE',
               #'ESCAPED_SINGLE_QUOTE',
               #'ESCAPED_DOUBLE_QUOTE',
               #'SINGLE_QUOTE',
               #'SINGLE_DOUBLE_QUOTE',
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

    #t_ESCAPED_SINGLE_QUOTE = r"\'"
    #t_ESCAPED_DOUBLE_QUOTE = r'\"'
    #t_SINGLE_QUOTE = r"'"
    #t_SINGLE_DOUBLE_QUOTE = r'"'
    #t_TRIPLE_QUOTE = r"'''"
    #t_TRIPLE_DOUBLE_QUOTE = r'"""'

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

def p_string(t):
    'string : SINGLE_QUOTE text SINGLE_QUOTE | SINGLE_DOUBLE_QUOTE text SINGLE_DOUBLE_QUOTE | TRIPLE_QUOTE text TRIPLE_QUOTE | TRIPLE_DOUBLE_QUOTE text TRIPLE_DOUBLE_QUOTE'
    pass
    
def p_error(t): 
    print "Syntax error at '%s'" % t.value 

'''
import ply.yacc as yacc 
yacc.yacc() 

while 1: 
    try: 
        s = raw_input('calc > ') 
    except EOFError: 
        break yacc.parse(s) 
'''

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

    return l.line_count() - l.empty_line_count, l.line_count()

if __name__ == '__main__':
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
