"""About scheme RFC6694

https://www.rfc-editor.org/rfc/rfc6694.html
"""

from typing import Any

import pyparsing as pp
from ppuri.component.fragment import Fragment
from ppuri.component.query import Query
from ppuri.exception import ParseError

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
    try:
        res = About.parse_string(text, parse_all=True)
        return res.as_dict()  # type: ignore
    except pp.ParseException as exc:
        raise ParseError(f"{text} is not a valid hostname") from exc


def scan(text: str) -> list[dict[str, str]]:
    uris: list[dict[str, str]] = []

    for tokens, start, end in About.scan_string(text):
        scan_result: dict[str, str] = tokens.as_dict()  # type: ignore
        scan_result["uri"] = text[start:end].strip("\n")
        uris.append(scan_result)

    return uris
