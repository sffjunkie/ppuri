import pytest
from ppuri.component.hostname import hostname_parse
from ppuri.exception import ParseError

good_hostnames = [
    ("example.com", "example.com"),
    ("www.example.com", "www.example.com"),
    ("www1.example.com", "www1.example.com"),
    ("www-1.example.com", "www-1.example.com"),
    ("[::1]", "::1"),
    ("192.168.1.1", "192.168.1.1"),
    ("8.8.8.8", "8.8.8.8"),
]

bad_hostnames = ["go!ogle.com", "1.1.1."]


@pytest.mark.parametrize("text,hostname", good_hostnames)
def test_hostname_parse_good(text: str, hostname: str):
    assert hostname_parse(text) == hostname  # type: ignore


@pytest.mark.parametrize("text", bad_hostnames)
def test_hostname_parse_bad(text: str):
    with pytest.raises(ParseError):
        hostname_parse(text)  # type: ignore
