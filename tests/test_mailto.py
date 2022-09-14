import pytest
from ppuri.scheme.mailto import to, MailTo


send_to_data = [
    ("job@example.com", ["job@example.com"]),
    ("job@example.com,me@example.org", ["job@example.com", "me@example.org"]),
]


@pytest.mark.parametrize("address_string,address_list", send_to_data)
def test_addresses(address_string: str, address_list: list[str]):
    res = to.parse_string(address_string).as_list()  # type: ignore
    assert address_list == res


# def test_mailto():
#     m = "mailto:joe@example.com,dave@example.com?a=2"
#     res = mailto.parse_string(m)
#     d = res.as_dict()

#     m = ""
#     res = mailto.parse_string(m)
#     d = res.as_dict()
#     pass


def test_mailto_single_address():
    m = "mailto:joe@example.com"
    res = MailTo.parse_string(m)
    d: dict[str, str] = res.as_dict()  # type: ignore
    assert len(d["addresses"]) == 1
    assert d["addresses"] == ["joe@example.com"]


def test_mailto_multiple_address():
    m = "mailto:joe@example.com,dave@example.com"
    res = MailTo.parse_string(m)
    d: dict[str, str] = res.as_dict()  # type: ignore
    assert len(d["addresses"]) == 2
    assert d["addresses"] == ["joe@example.com", "dave@example.com"]


def test_mailto_single_address_with_params():
    m = "mailto:joe@example.com?param1=2"
    res = MailTo.parse_string(m)
    d: dict[str, str] = res.as_dict()  # type: ignore
    assert len(d["parameters"]) == 1
    assert d["parameters"][0] == {"name": "param1", "value": "2"}


def test_mailto_multiple_address_with_params():
    m = "mailto:someone@yoursite.com,dave@example.com?cc=someoneelse@theirsite.com, another@thatsite.com, me@mysite.com&bcc=lastperson@theirsite.com&subject=Big%20News"
    res = MailTo.parse_string(m)
    d: dict[str, str] = res.as_dict()  # type: ignore
    assert len(d["parameters"]) == 3
    assert d["parameters"][0] == {
        "name": "cc",
        "value": "someoneelse@theirsite.com, another@thatsite.com, me@mysite.com",
    }
