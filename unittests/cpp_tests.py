import unittest

import pyloc.cpp_source as p

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
            
        self.assert_(self.l.line_count() == 0)
        self.assert_(self.l.empty_line_count == 0)


def suite():
    return unittest.TestLoader().loadTestsFromTestCase(LexerTests)

if __name__ == '__main__':
    unittest.main()
