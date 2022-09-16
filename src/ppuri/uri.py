"""URI parse/scan

https://www.rfc-editor.org/rfc/rfc3986
"""
from pathlib import Path
from typing import Any

from pyparsing import ParseException

from ppuri.exception import ParseError
from ppuri.scheme.aaa import AAA
from ppuri.scheme.about import About
from ppuri.scheme.coap import COAP
from ppuri.scheme.crid import Crid
from ppuri.scheme.data import Data
from ppuri.scheme.file import File
from ppuri.scheme.http import Http
from ppuri.scheme.mailto import MailTo
from ppuri.scheme.url import Url
from ppuri.scheme.urn import Urn
from ppuri.types import MatchLocation, ScanResult

Uri = Http ^ MailTo ^ File ^ AAA ^ About ^ COAP ^ Crid ^ Urn ^ Data | Url


def parse(text: str) -> dict[str, Any]:
    """Parse a URI into its components.

    Args:
        text: The text to parse as an URI

    Returns:
        A dictionary of URI components and values

    Raises:
        `ppuri.exception.ParseError` if text is not a valid URI
    """
    try:
        parse_result = Uri.parse_string(text, parse_all=True)
        parse_result = parse_result.as_dict()  # type: ignore
        parse_result["uri"] = text.strip("\n")
        return parse_result  # type: ignore
    except ParseException as exc:
        raise ParseError(f"{text} is not a valid URI") from exc


def scan(text: str) -> list[ScanResult]:
    """Scan a string for all URIs.

    Args:
        text: The text to scan for URIs

    Returns:
        A list of matching strings
    """
    uris: list[ScanResult] = []

    for tokens, start, end in Uri.scan_string(text):
        scan_result: ScanResult = tokens.as_dict()  # type: ignore
        scan_result["uri"] = text[start:end].strip("\n")
        scan_result["location"] = MatchLocation(1, start + 1)
        uris.append(scan_result)

    return uris


def scan_file(file: Path) -> list[ScanResult]:
    """Scan a file for all URIs.

    Args:
        file: A Path object for the file to scan for URIs

    Returns:
        A list of ScanResults
    """
    uris: list[ScanResult] = []

    with open(file, "r", encoding="utf-8") as fileptr:
        for line_number, line in enumerate(fileptr.readlines()):
            for tokens, start, end in Uri.scan_string(line):
                scan_result: ScanResult = tokens.as_dict()  # type: ignore
                scan_result["uri"] = line[start:end].strip("\n")
                scan_result["location"] = MatchLocation(line_number + 1, start + 1)
                uris.append(scan_result)

    return uris
