# type: ignore
import pyparsing as pp
import pytest
from ppuri.component import ipv4
from ppuri.exception import ParseError

good_octet = [str(i) for i in range(256)]
bad_octet = ["256"]

good_ip = [
    ("0.0.0.0", "0.0.0.0"),
    ("255.255.255.255", "255.255.255.255"),
]
bad_ip = [
    ("255.255.255.256"),
    ("255.255.255.-1"),
]


@pytest.mark.parametrize("octet", good_octet)
def test_good_octet(octet: str):
    _results = ipv4.segment.parse_string(octet)


@pytest.mark.parametrize("octet", bad_octet)
def test_bad_octet(octet: str):
    with pytest.raises(pp.ParseException):
        _results = ipv4.segment.parse_string(octet)


@pytest.mark.parametrize("text,ip", good_ip)
def test_ipv4_parse(text: str, ip: list[str]):
    results = ipv4.parse(text)
    assert results == ip  # type: ignore


@pytest.mark.parametrize("text", bad_ip)
def test_bad_ipv4_parse(text: str):
    with pytest.raises(ParseError):
        _results = ipv4.parse(text)


@pytest.mark.parametrize("text,ip", good_ip)
def test_ipv4_scan(text: str, ip: list[str]):
    results = ipv4.scan(f" IP address = {text}, and address 2 is {text}")
    assert len(results) == 2
    assert results[0] == ip


def test_scan_string_with_bad():
    text = "A bad IP address 10.0.0.256 and a good IP address 10.0.0.1"
    results = ipv4.scan(text)
    assert len(results) == 1
