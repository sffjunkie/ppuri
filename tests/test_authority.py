import pytest

# import pyparsing as pp

from ppuri.component.authority import Authority

authorities = [
    ("bbc.com", {"address": "bbc.com"}),
    ("bbc.com:443", {"address": "bbc.com", "port": "443"}),
    ("www.bbc.com:443", {"address": "www.bbc.com", "port": "443"}),
    ("www.bbc.com:442", {"address": "www.bbc.com", "port": "442"}),
    ("8.8.8.8:442", {"address": "8.8.8.8", "port": "442"}),
    ("[1:2:3:4:5:6:7:8]:442", {"address": "1:2:3:4:5:6:7:8", "port": "442"}),
]


@pytest.mark.parametrize("text,authority", authorities)
def test_authority_parse(text: str, authority: list[str]):
    res = Authority.parse_string(text, parse_all=True).as_dict()  # type: ignore
    assert res["authority"] == authority
