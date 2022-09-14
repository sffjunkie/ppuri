from ppuri.uri import Uri


def test_uri_scan():
    text = "A url https://example.com and a file file://google.txt and another https://google.com"
    results = list(Uri.scan_string(text))
    assert len(results) == 3
