from ppuri import uri


def test_uri_scan():
    text = "A url https://example.com and a file file://google.txt and another https://google.com"
    results = uri.scan(text)
    assert len(results) == 3
