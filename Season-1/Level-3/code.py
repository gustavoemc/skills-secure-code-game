# Welcome to Secure Code Game Season-1/Level-3!

# You know how to play by now, good luck!

import os
from flask import Flask, request

### Unrelated to the exercise -- Starts here -- Please ignore
app = Flask(__name__)
@app.route("/")
def source():
    TaxPayer('foo', 'bar').get_tax_form_attachment(request.args["input"])
    TaxPayer('foo', 'bar').get_prof_picture(request.args["input"])
### Unrelated to the exercise -- Ends here -- Please ignore

def safe_path(path):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.normpath(os.path.join(base_dir, path))
    if base_dir != os.path.commonpath([base_dir, filepath]):
        return None
    return filepath

class TaxPayer:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.prof_picture = None
        self.tax_form_attachment = None

    # returns the path of an optional profile picture that users can set
    def get_prof_picture(self, path=None):
        # setting a profile picture is optional
        if not path:
            return None

        # Secure the path using safe_path
        prof_picture_path = safe_path(path)
        if not prof_picture_path:
            return None

        try:
            with open(prof_picture_path, 'rb') as pic:
                picture = bytearray(pic.read())
            return prof_picture_path
        except FileNotFoundError:
            return None

    # returns the path of an attached tax form that every user should submit
    def get_tax_form_attachment(self, path=None):
        if not path:
            raise Exception("Error: Tax form is required for all users")

        # Secure the path using safe_path
        tax_form_path = safe_path(path)
        if not tax_form_path:
            raise Exception("Invalid path for tax form")

        try:
            with open(tax_form_path, 'rb') as form:
                tax_data = bytearray(form.read())
            return tax_form_path
        except FileNotFoundError:
            raise Exception("Tax form not found")
