import pyparsing as pp
from ppuri.component import ipv4
from ppuri.exception import ParseError

colon = pp.Literal(":")
ipv6_segment = pp.Word(pp.hexnums, min=1, max=4)

# https://stackoverflow.com/a/17871737/3253026
IPv6Address = pp.Combine(
    ((ipv6_segment + colon)[7, 7] + ipv6_segment)
    | ((ipv6_segment + colon)[1, 7] + colon)
    | ((ipv6_segment + colon)[1, 6] + colon + ipv6_segment)
    | ((ipv6_segment + colon)[1, 5] + colon + (colon + ipv6_segment)[1, 2])
    | ((ipv6_segment + colon)[1, 4] + colon + (colon + ipv6_segment)[1, 3])
    | ((ipv6_segment + colon)[1, 3] + colon + (colon + ipv6_segment)[1, 4])
    | ((ipv6_segment + colon)[1, 2] + colon + (colon + ipv6_segment)[1, 5])
    | ((ipv6_segment + colon)) + (colon + ipv6_segment)[1, 6]
    | colon + ((colon + ipv6_segment)[1, 7] | colon)
    | (
        pp.CaselessLiteral("fe80")
        + colon
        + (colon + pp.Optional(pp.Word(pp.hexnums, max=4)))[0, 4]
        + pp.Optional(pp.Literal("%") + pp.Word(pp.alphanums, min=1))
    )
    | (
        colon
        + colon
        + pp.Optional(
            pp.CaselessLiteral("ffff")
            + pp.Optional(colon + pp.Word("0", min=1, max=4))
            + colon
        )
        + ipv4.IPv4Address
    )
    | (ipv6_segment + colon)[1, 4] + colon + ipv4.IPv4Address
).set_results_name("address") + ~pp.FollowedBy(colon)


def parse(text: str) -> str:
    try:
        result = IPv6Address.parse_string(text)
        return result.as_dict()["address"]  # type: ignore
    except pp.ParseException as exc:
        raise ParseError(f"{text} is not a valid IPv6 address") from exc


def ipv6_scan(text: str) -> list[str]:
    try:
        res = IPv6Address.scan_string(text)
    except pp.ParseException:
        return []

    address: str
    addresses: list[str] = []
    for address in res.as_list():  # type: ignore
        addresses.append(address)

    return addresses
