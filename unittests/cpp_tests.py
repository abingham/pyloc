from cStringIO import StringIO
import unittest

import pyloc.cpp_source as p
print p

class LexerTests(unittest.TestCase):
    def setUp(self):
        self.l = p.LOCLexer()
        self.l.build()

    def tearDown(self):
        pass

    def basic_test(self, 
                   text, 
                   total, 
                   code, 
                   empty, 
                   comment):
        c = p.loc(StringIO(text))
        
        for tag in ['total', 'code', 'empty', 'comment']:
            exec("print '%s', %s, c['%s']" % (tag, tag, tag))

        self.assert_(c['total']     == total)
        self.assert_(c['code']      == code)
        self.assert_(c['empty']     == empty)
        self.assert_(c['comment']   == comment)
        
    def test_empty_file(self):
        self.basic_test(
            '',
            0,0,0,0)

    def test_all_blank(self):
        self.basic_test(
            '''


''',
            3, 0, 3, 0)

    def test_simple_function(self):
        self.basic_test(
            '''#include <foo.h>

/* A very, very
   complex function 
*/
int bar(Foo f) {
   int x = 1; // Assign one to x

   return x + 1;
} // end of function
''',
            10, 5, 2, 5)

    def test_compound_comments(self):
        self.basic_test(
            '''/* This is 
a multiline
comment */ // Followed by a regular
// comment
''',
            4, 0, 0, 4)

def suite():
    return unittest.TestLoader().loadTestsFromTestCase(LexerTests)

if __name__ == '__main__':
    unittest.main()
