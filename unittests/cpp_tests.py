import cStringIO, unittest

import pyloc.cpp_source as p

class LexerTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def basic_test(self,
                   text,
                   total,
                   code,
                   empty,
                   comment):
        c = p.loc(cStringIO.StringIO(text))

        #for tag in ['total', 'code', 'empty', 'comment']:
        #    exec("print '%s', %s, c['%s']" % (tag, tag, tag))

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

    def test_basic_code(self):
        self.basic_test(
            '''#include <llama.hpp>

/* This is a really critical
   function, so we'll keep
   it really simple */
int foo(float bar) {
  string x("asdf");
  return 2;
} // end of function
''',
            9, 5, 1, 4)

    def test_mixed_comments(self):
        self.basic_test(
            '''/* /* */
// /* //
/* // */


/*
  // // /*

*/

''',
            10, 0, 3, 7)
def suite():
    return unittest.TestLoader().loadTestsFromTestCase(LexerTests)

if __name__ == '__main__':
    unittest.main()
