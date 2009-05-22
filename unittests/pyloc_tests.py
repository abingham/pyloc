import unittest

from pyloc.util import loc

class Tests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_python(self):
        t1_expected = { 'data/test1.py' : ('data/test1.py', 'Python', {'comment': 2, 'code': 2, 'total': 5, 'docstring': 2, 'empty': 1}) }
        t2_expected = { 'data/test2.py' : ('data/test2.py', 'Python', {'comment': 1, 'code': 3, 'total': 5, 'docstring': 1, 'empty': 1}) }
        
        self.assert_(loc('data/test1.py') == t1_expected)
        self.assert_(loc('data/test2.py') == t2_expected)

    def test_python_dir(self):
        expected = { 'data/test1.py' : ('data', 'Python', { 'comment' : 2, 'code' : 2, 'total' : 5, 'docstring' : 2, 'empty' : 1 }),
                     'data/test2.py' : ('data', 'Python', { 'comment': 1, 'code': 3, 'total': 5, 'docstring': 1, 'empty': 1}) }
          
        self.assert_(loc('data') == expected)

def suite():
    return unittest.TestLoader().loadTestsFromTestCase(Tests)

if __name__ == '__main__':
    unittest.main()
