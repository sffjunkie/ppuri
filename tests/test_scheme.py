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
    ("urn:nid:n:s:s", "urn"),
]


@pytest.mark.parametrize("text,info", good_scheme_names)
def test_scheme_parse_good_scheme_name(text: str, info: str):
    assert scheme.parse(text) == info  # type: ignore
