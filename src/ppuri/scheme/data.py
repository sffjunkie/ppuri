"""The "data" URL scheme

https://www.rfc-editor.org/rfc/rfc2397.html
"""
from typing import Any

import pyparsing as pp
from ppuri import semicolon
from ppuri.component.media_type import MediaType
from ppuri.exception import ParseError
from ppuri.types import MatchLocation, ScanResult

colon = pp.Literal(":").suppress()

data_value = pp.Literal(",").suppress() + pp.Word(
    pp.alphas, pp.alphanums
).set_results_name("data")

Data = (
    pp.Literal(f"data").set_results_name("scheme")
    + colon
    + pp.Optional(MediaType)
    + pp.Optional(semicolon + pp.Literal("base64").set_results_name("encoding"))
    + data_value
)


def parse(text: str) -> dict[str, Any]:
    """Parse a `data` URI into its components.

    Args:
        text: The text to parse as an `data` URI

    Returns:
        A dictionary of URI components and values

    Raises:
        `ppuri.exception.ParseError` if text is not a valid `data` URI
    """
    try:
        res = Data.parse_string(text, parse_all=True)
        return res.as_dict()  # type: ignore
    except pp.ParseException as exc:
        raise ParseError(f"{text} is not a valid data URI") from exc


def scan(text: str) -> list[ScanResult]:
    """Scan a string for `data` URIs.

    Args:
        text: The text to scan for `data` URIs

    Returns:
        A list of ScanResults
    """
    uris: list[ScanResult] = []

    for tokens, start, end in Data.scan_string(text):
        scan_result: ScanResult = tokens.as_dict()  # type: ignore
        scan_result["uri"] = text[start:end].strip("\n")
        scan_result["location"] = MatchLocation(1, start + 1)
        uris.append(scan_result)

    return uris
