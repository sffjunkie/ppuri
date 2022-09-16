"""Diameter Base Protocol RFC6733

https://www.rfc-editor.org/rfc/rfc6733.html
"""

from typing import Any

import pyparsing as pp
from ppuri import authority_start
from ppuri.component.authority import Authority
from ppuri.exception import ParseError
from ppuri.types import MatchLocation, ScanResult

colon = pp.Literal(":").suppress()
semicolon = pp.Literal(";").suppress()

transports = pp.Literal("tcp") | pp.Literal("udp") | pp.Literal("utcp")
protocols = pp.Literal("diameter") | pp.Literal("radius") | pp.Literal("tacacs+")

transport = pp.Combine(
    semicolon + pp.Literal("transport=") + transports.set_results_name("transport")
)
protocol = pp.Combine(
    semicolon + pp.Literal("protocol=") + protocols.set_results_name("protocol")
)


def AAAf(suffix: str = "") -> pp.ParserElement:
    return pp.Combine(
        pp.CaselessLiteral(f"aaa{suffix}").set_results_name("scheme")
        + colon
        + authority_start
        + Authority
        + pp.Optional(transport)
        + pp.Optional(protocol)
    )


AAA = AAAf() ^ AAAf("s")


def parse(text: str) -> dict[str, Any]:
    """Parse an `aaa` URI into its components.

    Args:
        text: The text to parse as an `aaa` URI

    Returns:
        A dictionary of URI components and values

    Raises:
        `ppuri.exception.ParseError` if text is not a valid `aaa` URI
    """
    try:
        res = AAA.parse_string(text, parse_all=True)
        return res.as_dict()  # type: ignore
    except pp.ParseException as exc:
        raise ParseError(f"{text} is not a valid aaa URI") from exc


def scan(text: str) -> list[ScanResult]:
    """Scan a string for `aaa` URIs.

    Args:
        text: The text to scan for `aaa` URIs

    Returns:
        A list of matching strings
    """
    uris: list[ScanResult] = []

    for tokens, start, end in AAA.scan_string(text):
        scan_result: ScanResult = tokens.as_dict()  # type: ignore
        scan_result["uri"] = text[start:end].strip("\n")
        scan_result["location"] = MatchLocation(1, start + 1)
        uris.append(scan_result)

    return uris
