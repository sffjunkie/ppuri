"""Content-ID and Message-ID Uniform Resource Locators

https://www.rfc-editor.org/rfc/rfc2392.html
"""
from typing import Any

import pyparsing as pp
from ppuri import authority_start
from ppuri.component.authority import Authority
from ppuri.component.path import Path
from ppuri.exception import ParseError
from ppuri.types import MatchLocation, ScanResult

colon = pp.Literal(":").suppress()

Crid = (
    pp.Literal(f"crid").set_results_name("scheme")
    + colon
    + authority_start
    + Authority
    + Path
)


def parse(text: str) -> dict[str, Any]:
    """Parse an `crid` URI into its components.

    Args:
        text: The text to parse as an `crid` URI

    Returns:
        A dictionary of URI components and values

    Raises:
        `ppuri.exception.ParseError` if text is not a valid `crid` URI
    """
    try:
        res = Crid.parse_string(text, parse_all=True)
        return res.as_dict()  # type: ignore
    except pp.ParseException as exc:
        raise ParseError(f"{text} is not a valid CRID URI") from exc


def scan(text: str) -> list[ScanResult]:
    """Scan a string for `crid` URIs.

    Args:
        text: The text to scan for `crid` URIs

    Returns:
        A list of ScanResults
    """
    uris: list[ScanResult] = []

    for tokens, start, end in Crid.scan_string(text):
        scan_result: ScanResult = tokens.as_dict()  # type: ignore
        scan_result["uri"] = text[start:end].strip("\n")
        scan_result["location"] = MatchLocation(1, start + 1)
        uris.append(scan_result)

    return uris
