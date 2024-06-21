import unittest
import os
import importlib.util

# Load the local code.py module dynamically
spec = importlib.util.spec_from_file_location("code", os.path.join(os.path.dirname(__file__), 'code.py'))
code = importlib.util.module_from_spec(spec)
spec.loader.exec_module(code)

class TestTaxPayer(unittest.TestCase):
    # Example 1 - path traversal exploited on get_prof_picture
    def test_1(self):
        # creates tax payer object with dummy username and password
        test_obj = code.TaxPayer('username_test', 'password_test')
        # user input to the profile picture
        input_path = './../../../../../etc/passwd'
        # the output of the function upon processing user input
        output = test_obj.get_prof_picture(input_path)

        self.assertIsNone(output)

    # Example 2 - path traversal exploited on get_tax_form_attachment
    def test_2(self):
        # creates tax payer object with dummy username and password
        test_obj = code.TaxPayer('username_test', 'password_test')
        # gets base directory
        base_dir = os.path.dirname(os.path.abspath(__file__))
        # user input to the tax form attachment
        file_path = './../../../../../etc/passwd'
        # complete path for input
        input_path = base_dir + file_path

        with self.assertRaises(Exception) as context:
            test_obj.get_tax_form_attachment(input_path)

        self.assertTrue("Invalid path for tax form" in str(context.exception))

if __name__ == '__main__':
    unittest.main()
