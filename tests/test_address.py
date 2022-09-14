import pytest
from ppuri.component import address
from ppuri.exception import ParseError

good_addresses = [
    ("example.com", "example.com"),
    ("www.example.com", "www.example.com"),
    ("www1.example.com", "www1.example.com"),
    ("www-1.example.com", "www-1.example.com"),
    ("[::1]", "::1"),
    ("192.168.1.1", "192.168.1.1"),
    ("8.8.8.8", "8.8.8.8"),
]

bad_addresses = ["go!ogle.com", "1.1.1."]


@pytest.mark.parametrize("text,info", good_addresses)
def test_address_parse_good(text: str, info: str):
    assert address.parse(text) == info  # type: ignore


@pytest.mark.parametrize("text", bad_addresses)
def test_address_parse_bad(text: str):
    with pytest.raises(ParseError):
        address.parse(text)  # type: ignore
