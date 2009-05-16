import unittest

from pyloc.main import loc

class Tests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_python(self):
        self.assert_(loc('data/test1.py') == (4,5))
        self.assert_(loc('data/test2.py') == (4,5))

def suite():
    return unittest.TestLoader().loadTestsFromTestCase(Tests)

if __name__ == '__main__':
    unittest.main()
