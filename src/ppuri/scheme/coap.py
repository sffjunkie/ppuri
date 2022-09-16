"""Constrained Application Protocol (CoAP) URI scheme

https://www.rfc-editor.org/rfc/rfc7252.html
"""
from typing import Any

import pyparsing as pp
from ppuri import authority_start, colon
from ppuri.component.authority import Authority
from ppuri.component.path import Path
from ppuri.exception import ParseError
from ppuri.types import MatchLocation, ScanResult


def _COAPf(suffix: str = "") -> pp.ParserElement:
    return (
        pp.Literal(f"coap{suffix}").set_results_name("scheme")
        + colon
        + authority_start
        + Authority
        + Path
    )


COAP = (
    _COAPf()
    ^ _COAPf("+tcp")
    ^ _COAPf("+ws")
    ^ _COAPf("s")
    ^ _COAPf("s+tcp")
    ^ _COAPf("s+ws")
)


def parse(text: str) -> dict[str, Any]:
    """Parse an `coap` URI into its components.

    Args:
        text: The text to parse as an `coap` URI

    Returns:
        A dictionary of URI components and values

    Raises:
        `ppuri.exception.ParseError` if text is not a valid `coap` URI
    """
    try:
        res = COAP.parse_string(text, parse_all=True)
        return res.as_dict()  # type: ignore
    except pp.ParseException as exc:
        raise ParseError(f"{text} is not a valid COAP URI") from exc


def scan(text: str) -> list[ScanResult]:
    """Scan a string for `coap` URIs.

    Args:
        text: The text to scan for `coap` URIs

    Returns:
        A list of matching strings
    """
    uris: list[ScanResult] = []

    for tokens, start, end in COAP.scan_string(text):
        scan_result: ScanResult = tokens.as_dict()  # type: ignore
        scan_result["uri"] = text[start:end].strip("\n")
        scan_result["location"] = MatchLocation(1, start + 1)
        uris.append(scan_result)

    return uris
