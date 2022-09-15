from ppuri.scheme import url


def test_postgres_parse():
    text = "postgres://example.com:5432"
    results = url.parse(text)
    assert results["scheme"] == "postgres"
    assert results["authority"] == {"address": "example.com", "port": "5432"}


def test_postgres_scan():
    text = "A url postgres://example.com:5432 aaa"
    results = url.scan(text)
    assert len(results) == 1
