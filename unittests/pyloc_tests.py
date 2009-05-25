import unittest

from pyloc.db import Results
from pyloc.util import loc

class Tests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_python(self):
        t1_expected = {'comment': 2, 'code': 2, 'total': 5, 'docstring': 2, 'empty': 1}
        t2_expected = {'comment': 1, 'code': 3, 'total': 5, 'docstring': 1, 'empty': 1}
        
        r = Results()
        loc(['data/test1.py'], r)
        self.assert_(r.counts_by_type('Python') == t1_expected)

        r = Results()
        loc(['data/test2.py'], r)
        self.assert_(r.counts_by_type('Python') == t2_expected)

    def test_python_dir(self):
        expected = { 'comment' : 3, 
                     'code' : 5,
                     'total' : 10,
                     'docstring' : 3,
                     'empty' : 2 }

        r = Results()
        loc(['data'], r)
        self.assert_(r.counts_by_type('Python') == expected)

def suite():
    return unittest.TestLoader().loadTestsFromTestCase(Tests)

if __name__ == '__main__':
    unittest.main()
