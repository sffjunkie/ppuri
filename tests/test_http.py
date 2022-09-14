from ppuri.scheme.http import Http


def test_url_with_space():
    result = Http.parse_string("https://google.com aj")
    resd = result.as_dict()  # type: ignore
    assert resd["scheme"] == "https"
    assert resd["authority"]["address"] == "google.com"
