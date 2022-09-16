from pathlib import Path
from typing import cast
from ppuri import uri


def test_uri_parse_aaa():
    text = "aaa://example.com;transport=tcp;protocol=radius"
    results = uri.parse(text)
    assert results is not None
    assert results["scheme"] == "aaa"
    assert results["transport"] == "tcp"
    assert results["protocol"] == "radius"


def test_uri_parse_about():
    text = "about:blank"
    results = uri.parse(text)
    assert results is not None
    assert results["scheme"] == "about"
    assert results["token"] == "blank"


def test_uri_parse_coap():
    text = "coap://example.com"
    results = uri.parse(text)
    assert results is not None
    assert results["scheme"] == "coap"
    assert results["authority"] == {"address": "example.com"}


def test_uri_parse_crid():
    text = "crid://example.com/path"
    results = uri.parse(text)
    assert results is not None
    assert results["scheme"] == "crid"
    assert results["authority"] == {"address": "example.com"}
    assert results["path"] == "/path"


def test_uri_parse_data():
    text = "data:image/gif;base64,deadbeef"
    results = uri.parse(text)
    assert results is not None
    assert results["scheme"] == "data"
    assert results["type"] == "image"
    assert results["subtype"] == "gif"
    assert results["encoding"] == "base64"
    assert results["data"] == "deadbeef"


def test_uri_parse_file():
    text = "file:///absolute/path"
    results = uri.parse(text)
    assert results is not None
    assert results["scheme"] == "file"
    assert results["path"] == "/absolute/path"


def test_uri_parse_http():
    text = "https://www.example.com:443/a.path?q=aparam#afragment"
    results = uri.parse(text)
    assert results is not None
    assert results["scheme"] == "https"
    assert results["authority"] == {"address": "www.example.com", "port": "443"}
    assert results["path"] == "/a.path"
    assert results["parameters"] == [{"name": "q", "value": "aparam"}]
    assert results["fragment"] == "afragment"


def test_uri_parse_mailto():
    text = (
        "mailto:someone@yoursite.com,dave@example.com?"
        "cc=someoneelse@theirsite.com,another@thatsite.com,me@mysite.com&"
        "bcc=lastperson@theirsite.com&subject=Big%20News"
    )
    results = uri.parse(text)
    assert results is not None
    assert results["scheme"] == "mailto"
    assert len(results["parameters"]) == 3
    assert results["parameters"][0] == {
        "name": "cc",
        "value": "someoneelse@theirsite.com,another@thatsite.com,me@mysite.com",
    }


def test_uri_parse_url():
    text = "postgres://example.com:5432"
    results = uri.parse(text)
    assert results["scheme"] == "postgres"
    assert results["authority"] == {"address": "example.com", "port": "5432"}


def test_uri_parse_urn():
    text = "urn:nid:n:s:s"
    results = uri.parse(text)
    assert results["scheme"] == "urn"
    assert results["nid"] == "nid"
    assert results["nss"] == "n:s:s"


def test_uri_scan():
    text = "A url https://example.com and a file file://google.txt and another https://google.com"
    results = uri.scan(text)
    assert len(results) == 3


def test_uri_scan_file():
    test_file = Path(__file__).parent / "file" / "uri.txt"
    results = uri.scan_file(test_file)
    assert results is not None
    assert len(results) == 3
    loc = cast(uri.MatchLocation, results[0]["location"])
    assert loc.line == 2
    assert loc.column == 7
    loc = cast(uri.MatchLocation, results[2]["location"])
    assert loc.line == 3
