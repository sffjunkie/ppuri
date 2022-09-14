import pytest

from ppuri.scheme.urn import Urn

urn_data = [("urn:nid:n:s:s", {"scheme": "urn", "nid": "nid", "nss": "n:s:s"})]


@pytest.mark.parametrize("urn_string,info", urn_data)
def test_urn(urn_string: str, info: dict[str, str]):
    result = Urn.parse_string(urn_string)
    assert result.as_dict() == info  # type: ignore
