from main import print_hi


def test_print_hi():
    value = "test"
    expected = "Hi, test"
    assert print_hi(value) == expected
