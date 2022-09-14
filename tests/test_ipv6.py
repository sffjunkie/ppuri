import pytest
import pyparsing as pp
from ppuri.component.ipv6 import ipv6_parse

good_ipv6 = [
    "::0",
    "::1",
    "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
    "fe80::0023:4567:890a",
    "fe80::0023:4567:890a%eth0",
    "fe80::0023:4567:890a%1",
    "2001:db8:a0b:12f0::1",
    "2001:db8:3:4:5::192.0.2.33",
]

bad_ipv6 = [
    ":0",
    "2001:0db8:85a3:0000:0000:8a2e:0370:7334:9021",
    "2001:0db8:85a3:::8a2e:0370:7334",
    "2001:::::::7334",
]


@pytest.mark.parametrize("text", good_ipv6)
def test_ipv6_parse(text: str):
    _res = ipv6_parse(text)


@pytest.mark.parametrize("text", bad_ipv6)
def test_ipv6_parse_bad(text: str):
    with pytest.raises(pp.ParseException):
        _res = ipv6_parse(text)
        pass
