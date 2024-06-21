import os
from flask import Flask, request, abort

app = Flask(__name__)

@app.route("/")
def source():
    try:
        TaxPayer('foo', 'bar').get_tax_form_attachment(request.args["input"])
        TaxPayer('foo', 'bar').get_prof_picture(request.args["input"])
    except Exception as e:
        abort(400, str(e))

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

    def get_prof_picture(self, path=None):
        if not path:
            return None

        safe_filepath = safe_path(path)
        if not safe_filepath:
            return None

        try:
            with open(safe_filepath, 'rb') as pic:
                picture = bytearray(pic.read())
            return safe_filepath
        except FileNotFoundError:
            return None

    def get_tax_form_attachment(self, path=None):
        if not path:
            raise Exception("Tax form is required for all users")

        safe_filepath = safe_path(path)
        if not safe_filepath:
            raise Exception("Invalid path for tax form")

        try:
            with open(safe_filepath, 'rb') as form:
                tax_data = bytearray(form.read())
            return safe_filepath
        except FileNotFoundError:
            raise Exception("Tax form not found")

