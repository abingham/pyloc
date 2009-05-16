class LOCLexer:
    tokens = ( 'COMMENT',
               #'ESCAPED_SINGLE_QUOTE',
               #'ESCAPED_DOUBLE_QUOTE',
               #'SINGLE_QUOTE',
               #'SINGLE_DOUBLE_QUOTE',
               #'TRIPLE_QUOTE',
               #'TRIPLE_DOUBLE_QUOTE', 
               )

    def t_COMMENT(self, t):
        r'[\t\ ]*\#.*\n'
        self.line_count += 1
        if self.empty_line:
            self.comment_line_count += 1
        self.empty_line = True

    #t_ESCAPED_SINGLE_QUOTE = r"\'"
    #t_ESCAPED_DOUBLE_QUOTE = r'\"'
    #t_SINGLE_QUOTE = r"'"
    #t_SINGLE_DOUBLE_QUOTE = r'"'
    #t_TRIPLE_QUOTE = r"'''"
    #t_TRIPLE_DOUBLE_QUOTE = r'"""'

    def t_newline(self, t):
        r'[\t\ ]*\n'
        if self.empty_line:
            self.empty_line_count += 1
        self.line_count += 1
        self.empty_line = True

    def t_error(self, t):
        self.empty_line = False
        t.lexer.skip(1) 

    def build(self, **kwargs):
        import ply.lex
        self.lexer = ply.lex.lex(object=self,**kwargs)

    def __init__(self):
        self.line_count = 0
        self.empty_line_count = 0
        self.empty_line = True
        self.comment_line_count = 0

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

    return l.line_count - l.empty_line_count, l.line_count
