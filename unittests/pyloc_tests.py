import unittest

from pyloc.util import loc

class Tests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_python(self):
        t1_expected = {'comment': 2, 'code': 2, 'total': 5, 'docstring': 2, 'empty': 1}
        t2_expected = {'comment': 1, 'code': 3, 'total': 5, 'docstring': 1, 'empty': 1}
        t1 = loc('data/test1.py')
        t2 = loc('data/test2.py')

        self.assert_(len(t1) == len(t1_expected))
        self.assert_(len(t2) == len(t2_expected))
        self.assert_(len(t1) == len(t2))

        for k in t1.keys():
            self.assert_(t1[k] == t1_expected[k])
            self.assert_(t2[k] == t2_expected[k])

    def test_python_dir(self):
        expected = { 'comment' : 3, 'code' : 5, 'total' : 10, 'docstring' : 3, 'empty' : 2 }
        rslt = loc('data')
        self.assert_(len(rslt) == len(expected))
        for k in rslt.keys():
            self.assert_(rslt[k] == expected[k])

def suite():
    return unittest.TestLoader().loadTestsFromTestCase(Tests)

if __name__ == '__main__':
    unittest.main()
