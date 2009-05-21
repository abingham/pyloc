import cStringIO, unittest

import pyloc.python_source as p

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
                   comment, 
                   docstring):
        c = p.loc(cStringIO.StringIO(text))

        for tag in ['total', 'code', 'empty', 'comment', 'docstring']:
            exec("print '%s', %s, c['%s']" % (tag, tag, tag))

        self.assert_(c['total']     == total)
        self.assert_(c['code']      == code)
        self.assert_(c['empty']     == empty)
        self.assert_(c['comment']   == comment)
        self.assert_(c['docstring'] == docstring)

    def test_empty_file(self):
        self.basic_test(
            '',
            0, 0, 0, 0, 0)

    def test_simple(self):
        self.basic_test(
            '''def foo():
  """a docstring"""
  x = 1
''',
            3, 2, 0, 1, 1)
        
    def test_all_empty(self):
        self.basic_test(
            '''


''',
            3, 0, 3, 0, 0)

    def test_middle_line(self):
        self.basic_test(
            '''
asdf=3

''',
            3, 1, 2, 0, 0)

    def test_basic_comments(self):
        self.basic_test(
            '''def foo():
  # a comment
  x = 1 # comment for this line
  # another comment
  y = 3
''',
            5, 3, 0, 3, 0)

    def test_multiline_basic(self):
        self.basic_test(
            """def foo():
  '''this is 

a multi
line
comment'''

  '''technically, so is this'''
""",
            8, 1, 1, 6, 6)

    def test_multiline_hash(self):
        self.basic_test(
            """
def llama():
  ''' # this is 
part # of a 
# multiline
comment'''

  '''hopefully this all # works '''
""",
            8, 1, 2, 5, 5)

    def test_multiline_and_comment(self):
        self.basic_test(
            """def yak():
  '''basic docstring # no comment'''
  # regular comment
 
  x = 1 # another comment
  y = '''a multiline
non-docstring''' # this is a comment
  # as is this '''hehehe'''
  '''hmmmm''' # hahaha
""",
            9, 3, 1, 6, 2)

    def test_multiline_double_basic(self):
        self.basic_test(
            '''def foo():
  """this is 

a multi
line
comment"""

  """technically, so is this"""
''',
            8, 1, 1, 6, 6)

    def test_multiline_double_hash(self):
        self.basic_test(
            '''
def llama():
  """ # this is 
part # of a 
# multiline
comment"""

  """hopefully this all # works """
''',
            8, 1, 2, 5, 5)

    def test_multiline_double_and_comment(self):
        self.basic_test(
            '''def yak():
  """basic docstring # no comment"""
  # regular comment
 
  x = 1 # another comment
  y = """a multiline
non-docstring""" # this is a comment
  # as is this """hehehe"""
  """hmmmm""" # hahaha
''',
            9, 3, 1, 6, 2)

    def test_single_string_basic(self):
        self.basic_test(
            """def foo():
  'this is is a docstring'

  'as is this'
""",
            4, 1, 1, 2, 2)
        
    def test_single_string_hash(self):
        self.basic_test(
            """
 def llama():
   ' # this is a docstring '

   'hopefully this all # works '
 """,
            5, 1, 2, 2, 2)

    def test_single_string_and_comment(self):
        process_input(
            self.l,
            """def yak():
  'basic docstring # no comment'
  # regular comment
 
  x = 1 # another comment
  y = 'a string' # with a comment
  'a docstring' # followed by a comment
""")
        self.count_test(7, 3, 1, 5, 2)

    def test_double_string_basic(self):
        process_input(
            self.l,
            '''def foo():
  "this is is a docstring"

  "as is this"
''')
        self.count_test(4, 1, 1, 2, 2)
        
    def test_double_string_hash(self):
        process_input(
            self.l,
            '''
 def llama():
   " # this is a docstring "

   "hopefully this all # works "
 ''')
        self.count_test(5, 1, 2, 2, 2)

    def test_double_string_and_comment(self):
        process_input(
            self.l,
            '''def yak():
  "basic docstring # no comment"
  # regular comment
 
  x = 1 # another comment
  y = "a string" # with a comment
  "a docstring" # followed by a comment
''')
        self.count_test(7, 3, 1, 5, 2)

def suite():
    return unittest.TestLoader().loadTestsFromTestCase(LexerTests)

if __name__ == '__main__':
    unittest.main()
