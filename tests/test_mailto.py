import pytest
from ppuri.scheme import mailto


send_to_data = [
    ("job@example.com", ["job@example.com"]),
    ("job@example.com,me@example.org", ["job@example.com", "me@example.org"]),
]


@pytest.mark.parametrize("address_string,address_list", send_to_data)
def test_addresses(address_string: str, address_list: list[str]):
    res = mailto.MailToAddress.parse_string(address_string).as_list()  # type: ignore
    assert address_list == res


def test_mailto_single_address():
    m = "mailto:joe@example.com"
    res = mailto.parse(m)
    assert len(res["addresses"]) == 1
    assert res["addresses"] == ["joe@example.com"]


def test_mailto_multiple_address():
    m = "mailto:joe@example.com,dave@example.com"
    res = mailto.parse(m)
    assert len(res["addresses"]) == 2
    assert res["addresses"] == ["joe@example.com", "dave@example.com"]


def test_mailto_single_address_with_params():
    m = "mailto:joe@example.com?param1=2"
    res = mailto.parse(m)
    assert len(res["parameters"]) == 1
    assert res["parameters"][0] == {"name": "param1", "value": "2"}


def test_mailto_multiple_address_with_params():
    m = "mailto:someone@yoursite.com,dave@example.com?cc=someoneelse@theirsite.com, another@thatsite.com, me@mysite.com&bcc=lastperson@theirsite.com&subject=Big%20News"
    res = mailto.parse(m)
    assert len(res["parameters"]) == 3
    assert res["parameters"][0] == {
        "name": "cc",
        "value": "someoneelse@theirsite.com, another@thatsite.com, me@mysite.com",
    }
