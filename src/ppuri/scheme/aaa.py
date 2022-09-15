"""Diameter Base Protocol RFC6733

https://www.rfc-editor.org/rfc/rfc6733.html
"""

from typing import Any

import pyparsing as pp
from ppuri import authority_start
from ppuri.component.authority import Authority
from ppuri.exception import ParseError

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
    try:
        res = AAA.parse_string(text, parse_all=True)
        return res.as_dict()  # type: ignore
    except pp.ParseException as exc:
        raise ParseError(f"{text} is not a valid hostname") from exc


def scan(text: str) -> list[dict[str, str]]:
    uris: list[dict[str, str]] = []

    for tokens, start, end in AAA.scan_string(text):
        scan_result: dict[str, str] = tokens.as_dict()  # type: ignore
        scan_result["uri"] = text[start:end].strip("\n")
        uris.append(scan_result)

    return uris
