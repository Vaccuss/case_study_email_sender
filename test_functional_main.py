from main import *


class TestDataLoading:
    def test_extract_json_data(self):
        path = '/Users/dean/PycharmProjects/pi_exchange/data/email_template.json'
        testin = extract_data(path, json_file)
        expected = {
            'from': "The Marketing Team<marketing@example.com",
            "subject": "{{FIRST_NAME}}, a new product is being launched soon...",
            "mimeType": "text/plain",
            "body": "Hi {{TITLE}} {{FIRST_NAME}} {{LAST_NAME}},\nToday, {{TODAY}}, we would like to tell you that... Sincerely,\nThe Marketing Team"
        }
        assert testin == expected

    def test_read_csv(self):
        path = '/Users/dean/PycharmProjects/pi_exchange/data/customers.csv'
        testin = extract_data(path, csv_file)

        expected = [{'TITLE': 'Mr', 'FIRST_NAME': 'John', 'LAST_NAME': 'Smith', 'EMAIL': 'john.smith@example.com'},
                    {'TITLE': 'Mrs', 'FIRST_NAME': 'Michelle', 'LAST_NAME': 'Smith',
                     'EMAIL': 'michelle.smith@example.com'}]

        assert testin[:2] == expected


class TestEmail:
    tmpl = {
        "singleItemCase": "{{FIRST_NAME}},",
        "notInCase": "text/plain",
        "multipleCase": "{{TITLE}} {{FIRST_NAME}} {{LAST_NAME}}, {{TODAY}}"
    }
    insert_data = {
        'FIRST_NAME': "first_name_test",
        'TITLE': 'title_test',
        'LAST_NAME': 'last_name_test',
        'TODAY': "today_str_test"
    }
    correct_tmpl = {
        "singleItemCase": "{FIRST_NAME},",
        "notInCase": "text/plain",
        "multipleCase": "{TITLE} {FIRST_NAME} {LAST_NAME}, {TODAY}"
    }
    correct_email = {
        "singleItemCase": "first_name_test,",
        "notInCase": "text/plain",
        "multipleCase": "title_test first_name_test last_name_test, today_str_test"
    }

    def test_process_template(self):
        assert Email.process_template(self.tmpl) == self.correct_tmpl

    def test_apply(self):
        assert Email.apply(self.insert_data, self.correct_tmpl) == self.correct_email


class TestSender:
    data = [
        {
            'keyCase': 'has data'
        },
        {
            'keyCase': 'has multiple items'
        }
    ]
    simple_strategy = lambda location, email: email['keyCase']

    def test_apply_strategy(self):
        res = sender(self.data, self.simple_strategy)
        assert res == ['has data', 'has multiple items']

# class TestFullIntegration:

#
#
#
#
#
# def test_main():
#
#
#
# test_main()
