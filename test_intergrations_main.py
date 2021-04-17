import pytest
from main import main
import shutil
import os
import json
import csv

output_dir = 'output/'

template = 'data/email_template.json'
customers = 'data/customers.csv'

output_file_folder = output_dir + 'files/'
errors = output_dir + 'errors.csv'


def setup_module(module):
    print("SETUP")
    os.mkdir(output_dir)
    main(template, customers, output_file_folder, errors)


def teardown_module(module):
    print("TEARDOWN")
    shutil.rmtree(output_dir)


def test_correct_amt_email_files():
    files = os.listdir(output_file_folder)
    assert len(files) == 2


def test_correct_file():
    actual = {"from": "The Marketing Team<marketing@example.com",
              "subject": "John, a new product is being launched soon...", "mimeType": "text/plain",
              "body": "Hi Mr John Smith,\nToday, 17 Apr 2021, we would like to tell you that... Sincerely,\nThe Marketing Team"}
    with open(output_file_folder + '/John_Smith.json') as f:
        data = json.loads(f.read())
    assert data == actual


def test_errors_file_exists():
    assert os.path.isfile(errors)


def test_errors_file_correct():
    with open(errors, 'r') as f:
        data = [row for row in csv.DictReader(f)]

    assert len(data) == 2
