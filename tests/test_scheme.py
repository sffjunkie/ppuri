import pytest
from ppuri.component.scheme import parse_scheme, scan_scheme


good_schemes = [
    ("https:", "https"),
    ("postgres:", "postgres"),
    ("urn:", "urn"),
    ("x-private:", "x-private"),
    ("git+https:", "git+https"),
    ("iris.beep:", "iris.beep"),
    ("https://", "https"),
    ("https://www.example.com", "https"),
]

missing_schemes = [
    ("www.example.com", ""),
    ("www.example.com:443", ""),
]

bad_schemes = [
    "htt!ps:",
]

text_with_scheme: list[tuple[str, list[str]]] = [
    ("This is some text without a URI scheme www.example.com", []),
    ("This is some text with a URI scheme https://www.example.com", ["https"]),
    (
        "This is some text with 2 URI schemes https://www.example.com and urn:a:b:c:d",
        ["https", "urn"],
    ),
    ("This is some text without a valid URI scheme htt!ps://www.example.com", []),
]


@pytest.mark.parametrize("text,scheme", good_schemes)
def test_scheme_parse_good(text: str, scheme: str):
    assert parse_scheme(text) == scheme  # type: ignore


@pytest.mark.parametrize("text,scheme", missing_schemes)
def test_scheme_parse_missing(text: str, scheme: str):
    assert parse_scheme(text, "unknown") == "unknown"  # type: ignore


@pytest.mark.parametrize("text", bad_schemes)
def test_scheme_parse_bad(text: str):
    assert parse_scheme(text) == ""  # type: ignore


@pytest.mark.parametrize("text", bad_schemes)
def test_scheme_parse_bad_with_default(text: str):
    assert parse_scheme(text, "unknown") == "unknown"  # type: ignore


@pytest.mark.parametrize("text,schemes", text_with_scheme)
def test_scheme_scan(text: str, schemes: list[str]):
    assert scan_scheme(text) == schemes  # type: ignore
    pass
