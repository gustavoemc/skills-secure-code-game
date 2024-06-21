# Welcome to Secure Code Game Season-1/Level-3!

# You know how to play by now, good luck!
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

class TaxPayer:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.prof_picture = None
        self.tax_form_attachment = None

    def get_prof_picture(self, path=None):
        if not path:
            return None
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        safe_path = self.secure_path(base_dir, path)

        if not safe_path:
            return None

        try:
            with open(safe_path, 'rb') as pic:
                picture = bytearray(pic.read())
            return safe_path
        except FileNotFoundError:
            return None

    def get_tax_form_attachment(self, path=None):
        if not path:
            raise Exception("Tax form is required for all users")

        base_dir = os.path.dirname(os.path.abspath(__file__))
        safe_path = self.secure_path(base_dir, path)

        if not safe_path:
            raise Exception("Invalid path for tax form")

        try:
            with open(safe_path, 'rb') as form:
                tax_data = bytearray(form.read())
            return safe_path
        except FileNotFoundError:
            raise Exception("Tax form not found")

    @staticmethod
    def secure_path(base_dir, path):
        normalized_path = os.path.normpath(os.path.join(base_dir, path))

        if os.path.commonpath([normalized_path, base_dir]) != base_dir:
            return None
        return normalized_path
