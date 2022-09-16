from typing import Any

import pyparsing as pp
from ppuri.exception import ParseError
from ppuri.types import MatchLocation, ScanResult

colon = pp.Literal(":").suppress()
nid = pp.Word(pp.alphanums, pp.alphanums + "-", min=1, max=31).set_results_name("nid")

reserved = "%/?#"
other = "()+,-.:=@;$_!*'"
trans = pp.alphanums + other + reserved

nss = pp.Word(trans).set_results_name("nss")

Urn = pp.CaselessLiteral("urn").set_results_name("scheme") + colon + nid + colon + nss


def parse(text: str) -> dict[str, Any]:
    """Parse a URN into its components.

    Args:
        text: The text to parse as an URN

    Returns:
        A dictionary of URI components and values

    Raises:
        `ppuri.exception.ParseError` if text is not a valid URN
    """
    try:
        parse_result = Urn.parse_string(text)
        parse_result = parse_result.as_dict()  # type: ignore
        parse_result["uri"] = text.strip("\n")
        return parse_result  # type: ignore
    except pp.ParseException as exc:
        raise ParseError(f"{text} is not a valid URN") from exc


def scan(text: str) -> list[ScanResult]:
    """Scan a string for URNs.

    Args:
        text: The text to scan for URNs

    Returns:
        A list of matching strings
    """
    uris: list[ScanResult] = []

    for tokens, start, end in Urn.scan_string(text):
        scan_result: ScanResult = tokens.as_dict()  # type: ignore
        scan_result["uri"] = text[start:end].strip("\n")
        scan_result["location"] = MatchLocation(1, start + 1)
        uris.append(scan_result)

    return uris
