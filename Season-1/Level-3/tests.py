import unittest
import os
import importlib.util

# Load the local code.py module
spec = importlib.util.spec_from_file_location("code", os.path.join(os.path.dirname(__file__), 'code.py'))
code = importlib.util.module_from_spec(spec)
spec.loader.exec_module(code)

class TestTaxPayer(unittest.TestCase):
    # Example 1 - shows a valid path to a profile picture
    def test_1(self):
        # creates tax payer object with dummy username and password
        test_obj = code.TaxPayer('username_test', 'password_test')
        # user input to the profile picture
        input_path = 'assets/prof_picture.png'
        # the output of the function upon processing user input
        output = test_obj.get_prof_picture(input_path)

        # the original function the method uses to come up with base directory
        original_base_dir = os.path.dirname(os.path.abspath(__file__))
        # the base directory that the code points on AFTER user input is supplied
        # the trick here is to use the length of the original directory counting from left
        resulted_based_dir = output[:len(os.path.dirname(os.path.abspath(__file__)))]

        # checks against path traversal by comparing the original to resulted directory
        self.assertEqual(original_base_dir, resulted_based_dir)

    # Example 2 - shows a valid path to a tax form
    def test_2(self):
        # creates tax payer object with dummy username and password
        test_obj = code.TaxPayer('username_test', 'password_test')
        # gets base directory
        base_dir = os.path.dirname(os.path.abspath(__file__))
        # user input to the tax form
        file_path = 'assets/tax_form.pdf'
        # complete path for input
        input_path = os.path.join(base_dir, file_path)
        # the output of the function upon processing user input
        output = test_obj.get_tax_form_attachment(input_path)

        # the original function the method uses to come up with base directory
        original_base_dir = os.path.dirname(os.path.abspath(__file__))
        # the base directory that the code points on AFTER user input is supplied
        # the trick here is to use the length of the original directory counting from left
        resulted_based_dir = output[:len(os.path.dirname(os.path.abspath(__file__)))]

        # checks against path traversal by comparing the original to resulted directory
        self.assertEqual(original_base_dir, resulted_based_dir)

if __name__ == '__main__':
    unittest.main(False)
