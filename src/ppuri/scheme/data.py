from typing import Any

import pyparsing as pp
from ppuri import semicolon
from ppuri.component.media_type import MediaType
from ppuri.exception import ParseError

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
    try:
        res = Data.parse_string(text, parse_all=True)
        return res.as_dict()  # type: ignore
    except pp.ParseException as exc:
        raise ParseError(f"{text} is not a valid hostname") from exc


def scan(text: str) -> list[dict[str, str]]:
    uris: list[dict[str, str]] = []

    for tokens, start, end in Data.scan_string(text):
        scan_result: dict[str, str] = tokens.as_dict()  # type: ignore
        scan_result["uri"] = text[start:end].strip("\n")
        uris.append(scan_result)

    return uris
