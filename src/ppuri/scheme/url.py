"""A generic URL

https://www.rfc-editor.org/rfc/rfc3986
"""

from typing import Any

import pyparsing as pp
from ppuri import (
    authority_start,
    colon,
    scheme_characters_next,
    scheme_characters_start,
)
from ppuri.component.authority import Authority
from ppuri.component.fragment import Fragment
from ppuri.component.path import Path
from ppuri.component.query import Query
from ppuri.exception import ParseError
from ppuri.types import MatchLocation, ScanResult

scheme_name = pp.Word(scheme_characters_start, scheme_characters_next)
UrlScheme = pp.Combine(scheme_name + colon)


Url = (
    UrlScheme.set_results_name("scheme")
    + authority_start
    + Authority
    + pp.Optional(Path)
    + pp.Optional(Query)
    + pp.Optional(Fragment)
)


def parse(text: str) -> dict[str, Any]:
    """Parse a generic URL into its components.

    Args:
        text: The text to parse as an generic URL

    Returns:
        A dictionary of URI components and values

    Raises:
        `ppuri.exception.ParseError` if text is not a valid generic URL
    """
    try:
        parse_result = Url.parse_string(text)
        parse_result = parse_result.as_dict()  # type: ignore
        parse_result["uri"] = text.strip("\n")
        return parse_result  # type: ignore
    except pp.ParseException as exc:
        raise ParseError(f"{text} is not a valid URL") from exc


def scan(text: str) -> list[ScanResult]:
    """Scan a string for generic URLs.

    Args:
        text: The text to scan for generic URLs

    Returns:
        A list of matching strings
    """
    uris: list[ScanResult] = []

    for tokens, start, end in Url.scan_string(text):
        scan_result: ScanResult = tokens.as_dict()  # type: ignore
        scan_result["uri"] = text[start:end].strip("\n")
        scan_result["location"] = MatchLocation(1, start + 1)
        uris.append(scan_result)

    return uris
