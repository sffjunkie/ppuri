"""HTTP/HTTPS URLs

https://www.rfc-editor.org/rfc/rfc9110.html
"""
from typing import Any

import pyparsing as pp
from ppuri import authority_start, colon
from ppuri.component.authority import Authority
from ppuri.component.fragment import Fragment
from ppuri.component.path import Path
from ppuri.component.query import Query
from ppuri.exception import ParseError
from ppuri.types import MatchLocation, ScanResult

Http = (
    (pp.CaselessLiteral("https") | pp.CaselessLiteral("http")).set_results_name(
        "scheme"
    )
    + colon
    + authority_start
    + Authority
    + pp.Optional(Path)
    + pp.Optional(Query)
    + pp.Optional(Fragment)
)


def parse(text: str) -> dict[str, Any]:
    """Parse a `http`/`https` URL into its components.

    Args:
        text: The text to parse as an `http` / `https` URL

    Returns:
        A dictionary of URI components and values

    Raises:
        `ppuri.exception.ParseError` if text is not a valid `http` / `https` URI
    """
    try:
        res = Http.parse_string(text, parse_all=True)
        return res.as_dict()  # type: ignore
    except pp.ParseException as exc:
        raise ParseError(f"{text} is not a valid http/https URL") from exc


def scan(text: str) -> list[ScanResult]:
    """Scan a string for `http` / `https` URLs.

    Args:
        text: The text to scan for `http` / `https` URLs

    Returns:
        A list of ScanResults
    """
    uris: list[ScanResult] = []

    for tokens, start, end in Http.scan_string(text):
        scan_result: ScanResult = tokens.as_dict()  # type: ignore
        scan_result["uri"] = text[start:end].strip("\n")
        scan_result["location"] = MatchLocation(1, start + 1)
        uris.append(scan_result)

    return uris
