''' This runs all of the unittests in py3db.
'''

import unittest

import pyloc_tests
import python_tests

sub_suites = [pyloc_tests.suite(),
              python_tests.suite()]

suite = unittest.TestSuite(sub_suites)

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite)
