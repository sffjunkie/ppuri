import pytest
from ppuri.component import scheme


good_scheme_names = [
    ("https:", "https"),
    ("postgres:", "postgres"),
    ("urn:", "urn"),
    ("x-private:", "x-private"),
    ("git+https:", "git+https"),
    ("iris.beep:", "iris.beep"),
    ("https://", "https"),
    ("https://www.example.com", "https"),
]

good_schemes = [
    ("urn:nid:n:s:s", "urn"),
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
]


@pytest.mark.parametrize("text,info", good_schemes)
def test_scheme_parse_good_scheme(text: str, info: str):
    result = scheme.parse(text)  # type: ignore
    assert result == info


@pytest.mark.parametrize("text,info", good_scheme_names)
def test_scheme_parse_good_scheme_name(text: str, info: str):
    assert scheme.parse(text) == info  # type: ignore


@pytest.mark.parametrize("text,info", missing_schemes)
def test_scheme_parse_missing_scheme_name(text: str, info: str):
    assert scheme.parse(text, "unknown") == "unknown"  # type: ignore


@pytest.mark.parametrize("text", bad_schemes)
def test_scheme_parse_bad_scheme_name(text: str):
    assert scheme.parse(text) == ""  # type: ignore


@pytest.mark.parametrize("text", bad_schemes)
def test_scheme_parse_bad_scheme_name_with_default(text: str):
    assert scheme.parse(text, "unknown") == "unknown"  # type: ignore
