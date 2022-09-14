import pytest
from ppuri.component.media_type import MediaType


media_type_data = [("image/gif", "image/gif")]


@pytest.mark.parametrize("data,value", media_type_data)
def test_media_type(data: str, value: str):
    result = MediaType.parse_string(data)
    assert result[0] == value


def test_mediatype_x():
    result = MediaType.parse_string("x-custom/x-mediatype")
    assert result[0] == "x-custom/x-mediatype"
