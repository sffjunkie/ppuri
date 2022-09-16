from typing import NamedTuple


class MatchLocation(NamedTuple):
    line: int
    column: int


ScanResult = dict[str, str | MatchLocation]
