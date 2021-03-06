import cStringIO

from ply.lex import TOKEN

class LOCLexer(object):
    tokens = ( 'BLOCK_COMMENT',
               'COMMENT',
               'CODE',
               )

    space = r'[\t\ ]*'
    

    @TOKEN(r'/\*(\n|.)*?\*/')
    def t_BLOCK_COMMENT(self, t):
        lines = len(t.value.split('\n'))
        if not self.comment_line:
            self.comment_line = True
            self.comment_line_count += lines
        else:
            self.comment_line_count += lines - 1

        self.empty_line = False
        self.lexer.lineno += lines - 1

    @TOKEN(r'//.*')
    def t_COMMENT(self, t):
        if not self.comment_line:
            self.comment_line_count += 1
        self.empty_line = False

    @TOKEN(r'\n')
    def t_newline(self, t):
        if self.empty_line:
            self.empty_line_count += 1
        self.lexer.lineno += 1
        self.empty_line = True
        self.comment_line = False
        self.code_line = False

    def t_error(self, t):
        if not self.code_line:
            self.code_line = True
            self.code_line_count += 1
        self.empty_line = False
        t.lexer.skip(1)

    def line_count(self):
        return self.lexer.lineno - 1

    def build(self, **kwargs):
        import ply.lex
        self.lexer = ply.lex.lex(object=self, **kwargs)
        
    def __init__(self):
        self.empty_line_count = 0
        self.empty_line = True

        self.comment_line_count = 0
        self.comment_line = False

        self.code_line_count = 0
        self.code_line = False

def loc(f):
    '''count lines of code in c++ files'''
    
    l = LOCLexer()
    l.build()
    l.lexer.input(f.read())
    while True:
        tok = l.lexer.token()
        if not tok: break

    line_count = l.lexer.lineno - 1
    return { 'total' : line_count,
             'code' : l.code_line_count,
             'empty' : l.empty_line_count,
             'comment' : l.comment_line_count, }

if __name__ == '__main__':
    '''a simple spot-test harness'''
    l = LOCLexer()
    l.build()

    io = cStringIO.StringIO()
    io.write(open('test_data.cpp', 'r').read())
    l.lexer.input(io.getvalue())
    while True:
        tok = l.lexer.token()
        if not tok: break
        
    print io.getvalue()
    print 'total:',    l.lexer.lineno - 1
    print 'empty:',    l.empty_line_count
    print 'comment:',  l.comment_line_count
