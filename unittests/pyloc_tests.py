import unittest

from pyloc.main import loc

class Tests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_python(self):
        t1_expected = {'comment': 0, 'minimum': 2, 'total': 5, 'docstring': 2, 'empty': 1}
        t2_expected = {'comment': 0, 'minimum': 3, 'total': 5, 'docstring': 1, 'empty': 1}
        t1 = loc('data/test1.py')
        t2 = loc('data/test2.py')

        self.assert_(len(t1) == len(t1_expected))
        self.assert_(len(t2) == len(t2_expected))
        self.assert_(len(t1) == len(t2))

        for k in t1.keys():
            self.assert_(t1[k] == t1_expected[k])
            self.assert_(t2[k] == t2_expected[k])

def suite():
    return unittest.TestLoader().loadTestsFromTestCase(Tests)

if __name__ == '__main__':
    unittest.main()
