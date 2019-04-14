import glob
import unittest

"""
Boilerplate code that can be used by ../run_tests.py to create a test_suite of all tests in directory. Note that it only
includes tests that follow the naming format 'tests/test_*.py'
"""


def create_test_suite():
    test_file_strings = glob.glob('test_*.py')
    # print('all_tests.create_test_suite.modules :', [string[6:len(string)-3] for string in test_file_strings])
    module_strings = ['tests.' + string[6:len(string)-3] for string in test_file_strings]
    # print('all_tests.create_test_suite.module_strings:', module_strings)
    suites = [unittest.defaultTestLoader.loadTestsFromName(name) \
              for name in module_strings]
    test_suite = unittest.TestSuite(suites)
    return test_suite
