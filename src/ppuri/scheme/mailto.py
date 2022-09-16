"""The 'mailto' URI Scheme

https://www.rfc-editor.org/rfc/rfc6068.html / https://www.rfc-editor.org/rfc/rfc5322.html"""
from typing import Any

import pyparsing as pp
from ppuri.component.query import Query
from ppuri.exception import ParseError
from ppuri.types import MatchLocation, ScanResult

FWS = pp.ZeroOrMore(pp.Literal(" \t")) + pp.LineEnd() + pp.OneOrMore(pp.Literal(" \t"))

vchar_ords = list(range(33, 127))
vchar = "".join(chr(c) for c in vchar_ords)

qtext_ords = [33] + list(range(35, 92)) + list(range(93, 127))
qtext = "".join(chr(c) for c in qtext_ords)

colon = pp.Literal(":").suppress()

atext = pp.alphanums + "!#$%&'*+-/=^_`{|}~"
atom = pp.Word(atext)
dot_atom_text = pp.Combine(atom + pp.ZeroOrMore("." + atom))

quoted_string = pp.Literal("\\") + (pp.Word(" \t" + vchar))

local_part = dot_atom_text | quoted_string

dtext_no_obs_ords = list(range(33, 91)) + list(range(94, 127))
dtext_no_obs = "".join(chr(c) for c in dtext_no_obs_ords)
domain = dot_atom_text | (pp.Literal("[") + dtext_no_obs + pp.Literal("]"))

addr_spec = pp.Combine(local_part + pp.Literal("@") + domain).set_results_name(
    "addresses*"
)

MailToAddress = addr_spec + pp.Optional(pp.Literal(",").suppress() + addr_spec)

MailTo = (
    pp.CaselessLiteral("mailto").set_results_name("scheme")
    + colon
    + MailToAddress
    + pp.Optional(Query)
)


def parse(text: str) -> dict[str, Any]:
    """Parse a `mailto` URI into its components.

    Args:
        text: The text to parse as an `mailto` URI

    Returns:
        A dictionary of URI components and values

    Raises:
        `ppuri.exception.ParseError` if text is not a valid `mailto` URI
    """
    try:
        res = MailTo.parse_string(text, parse_all=True)
        return res.as_dict()  # type: ignore
    except pp.ParseException as exc:
        raise ParseError(f"{text} is not a valid mailto URI") from exc


def scan(text: str) -> list[ScanResult]:
    """Scan a string for `mailto` URIs.

    Args:
        text: The text to scan for `mailto` URIs

    Returns:
        A list of matching strings
    """
    uris: list[ScanResult] = []

    for tokens, start, end in MailTo.scan_string(text):
        scan_result: ScanResult = tokens.as_dict()  # type: ignore
        scan_result["uri"] = text[start:end].strip("\n")
        scan_result["location"] = MatchLocation(1, start + 1)
        uris.append(scan_result)

    return uris
