import json
import csv
from datetime import date
import sys
import re
import os


def validate_customers(customers):
    email_regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
    valids = []
    errors = []
    for c in customers:
        valids.append(c) if re.search(email_regex, c["EMAIL"]) else errors.append(c)

    return valids, errors


# Reading section - tested
def json_file(file):
    return json.loads(file.read())


def csv_file(file):
    return [row for row in csv.DictReader(file)]


def extract_data(path, process_fn):
    with open(path, 'r') as f:
        data = process_fn(f)
    return data


# Generation section
class Email(object):
    __slots__ = 'value', 'customer'

    def __init__(self, template, customer):
        customer['TODAY'] = date.today().strftime("%d %b %Y")  # format: 31 Dec 2020
        self.customer = customer
        template = self.process_template(template)
        self.value = self.apply(customer, template)

    @staticmethod
    def apply(customer, processed_template):
        return {k: v.format(**customer) for (k, v) in processed_template.items()}

    @staticmethod
    def process_template(template):
        return {k: v.replace('{{', '{').replace('}}', '}') for (k, v) in template.items()}


# Sender section
def to_file_strategy(location):
    def inner(email):
        filename = '{}_{}.json'.format(email.customer['FIRST_NAME'], email.customer['LAST_NAME'])
        outpath = location + filename
        print(outpath)
        try:
            with open(outpath, 'w') as outfile:
                json.dump(email.value, outfile)
            return 'succeed'
        except IOError:
            return 'IOError: Write Failure: ' + email.customer['EMAIL']

    return inner


def sender(emails, strategy_fn):
    res = []
    for email in emails:
        res.append(strategy_fn(email))
    return res


# Errors section
def write_errors(location, errors):
    names = errors[0].keys()
    try:
        with open(location, 'w') as f:
            writer = csv.DictWriter(f, fieldnames=names)
            writer.writeheader()
            for e in errors:
                writer.writerow(e)
    except IOError:
        raise IOError


def ensure_directory(output_dir):
    try:
        os.mkdir(output_dir)
        return output_dir
    except FileExistsError:
        return "Exists"


# Main
def main(*args):
    template = extract_data(args[0], json_file)
    customers = extract_data(args[1], csv_file)
    output_path = ensure_directory(args[2])
    errors_path = args[3]

    customers, errors = validate_customers(customers)
    emails = [Email(template, customer) for customer in customers]

    sender(emails, to_file_strategy(location=output_path))
    write_errors(errors_path, errors)


if __name__ == '__main__':
    main(*sys.argv[1:])
