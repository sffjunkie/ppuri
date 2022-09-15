from typing import Any

import pyparsing as pp
from ppuri import authority_start
from ppuri.component.authority import Authority
from ppuri.component.path import Path
from ppuri.exception import ParseError

colon = pp.Literal(":").suppress()

Crid = (
    pp.Literal(f"crid").set_results_name("scheme")
    + colon
    + authority_start
    + Authority
    + Path
)


def parse(text: str) -> dict[str, Any]:
    try:
        res = Crid.parse_string(text, parse_all=True)
        return res.as_dict()  # type: ignore
    except pp.ParseException as exc:
        raise ParseError(f"{text} is not a valid hostname") from exc


def scan(text: str) -> list[dict[str, str]]:
    uris: list[dict[str, str]] = []

    for tokens, start, end in Crid.scan_string(text):
        scan_result: dict[str, str] = tokens.as_dict()  # type: ignore
        scan_result["uri"] = text[start:end].strip("\n")
        uris.append(scan_result)

    return uris
