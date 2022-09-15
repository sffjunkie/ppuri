"""The "file" URI Scheme

https://www.rfc-editor.org/rfc/rfc8089.html
"""
from typing import Any

import pyparsing as pp
from ppuri import authority_start, colon, path_characters, path_start
from ppuri.exception import ParseError

FilePath = pp.Combine(
    pp.Optional(path_start) + pp.Word(pp.alphanums, path_characters)
).set_results_name("path")

File = (
    pp.CaselessLiteral("file").set_results_name("scheme")
    + colon
    + authority_start
    + FilePath
)


def parse(text: str) -> dict[str, Any]:
    """Parse a `file` URI into its components.

    Args:
        text: The text to parse as an `file` URI

    Returns:
        A dictionary of URI components and values

    Raises:
        `ppuri.exception.ParseError` if text is not a valid `file` URI
    """
    try:
        res = File.parse_string(text, parse_all=True)
        return res.as_dict()  # type: ignore
    except pp.ParseException as exc:
        raise ParseError(f"{text} is not a valid file URI") from exc


def scan(text: str) -> list[dict[str, str]]:
    """Scan a string for `file` URIs.

    Args:
        text: The text to scan for `file` URIs

    Returns:
        A list of matching strings
    """
    uris: list[dict[str, str]] = []

    for tokens, start, end in File.scan_string(text):
        scan_result: dict[str, str] = tokens.as_dict()  # type: ignore
        scan_result["uri"] = text[start:end].strip("\n")
        uris.append(scan_result)

    return uris
