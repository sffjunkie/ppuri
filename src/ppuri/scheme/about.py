"""About URI scheme

https://www.rfc-editor.org/rfc/rfc6694.html
"""

from typing import Any

import pyparsing as pp
from ppuri.component.fragment import Fragment
from ppuri.component.query import Query
from ppuri.exception import ParseError
from ppuri.types import MatchLocation, ScanResult

colon = pp.Literal(":").suppress()
semicolon = pp.Literal(";").suppress()

tokens = pp.Literal("blank").set_results_name("token")

About = pp.Combine(
    pp.CaselessLiteral("about").set_results_name("scheme")
    + colon
    + tokens
    + pp.Optional(Query)
    + pp.Optional(Fragment)
)


def parse(text: str) -> dict[str, Any]:
    """Parse an `about` URI into its components.

    Args:
        text: The text to parse as an `about` URI

    Returns:
        A dictionary of URI components and values

    Raises:
        `ppuri.exception.ParseError` if text is not a valid `about` URI
    """
    try:
        res = About.parse_string(text, parse_all=True)
        return res.as_dict()  # type: ignore
    except pp.ParseException as exc:
        raise ParseError(f"{text} is not a valid `about` URI") from exc


def scan(text: str) -> list[ScanResult]:
    """Scan a string for `about` URIs.

    Args:
        text: The text to scan for `about` URIs

    Returns:
        A list of ScanResults
    """
    uris: list[ScanResult] = []

    for tokens, start, end in About.scan_string(text):
        scan_result: ScanResult = tokens.as_dict()  # type: ignore
        scan_result["uri"] = text[start:end].strip("\n")
        scan_result["location"] = MatchLocation(1, start + 1)
        uris.append(scan_result)

    return uris
