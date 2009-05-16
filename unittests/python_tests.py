import unittest

import pyloc.python as p

def process_input(l, input):
    l.lexer.input(input)
    while True:
        tok = l.lexer.token()
        if not tok: break

class LexerTests(unittest.TestCase):
    def setUp(self):
        self.l = p.LOCLexer()
        self.l.build()

    def tearDown(self):
        pass

    def test_empty_file(self):
        process_input(self.l, '')
            
        self.assert_(self.l.line_count == 0)
        self.assert_(self.l.empty_line_count == 0)

    def test_simple(self):
        process_input(
            self.l,
            '''def foo():
  """a docstring"""
  x = 1
''')
        self.assert_(self.l.line_count == 3)
        self.assert_(self.l.empty_line_count == 0)
        
    def test_all_empty(self):
        process_input(
            self.l,
            '''


''')
        self.assert_(self.l.line_count == 3)
        self.assert_(self.l.empty_line_count == self.l.line_count)

    def test_middle_line(self):
        process_input(
            self.l,
            '''
asdf

''')
        self.assert_(self.l.line_count == 3)
        self.assert_(self.l.empty_line_count == 2)

    def test_basic_comments(self):
        process_input(
            self.l,
            '''def foo():
  # a comment
  x = 1 # comment for this line
  # another comment
  y = 3
''')
        self.assert_(self.l.line_count == 5)
        self.assert_(self.l.empty_line_count == 0)
        self.assert_(self.l.comment_line_count == 2)

def suite():
    return unittest.TestLoader().loadTestsFromTestCase(LexerTests)

if __name__ == '__main__':
    unittest.main()
