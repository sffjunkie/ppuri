import pytest
from ppuri.scheme.data import Data

data_type_data = [
    (
        "data:image/gif,deadbeef",
        {"scheme": "data", "type": "image", "subtype": "gif", "data": "deadbeef"},
    ),
    (
        "data:image/gif;base64,deadbeef",
        {
            "scheme": "data",
            "type": "image",
            "subtype": "gif",
            "encoding": "base64",
            "data": "deadbeef",
        },
    ),
    (
        "data:image/gif;base64,base64data",
        {
            "scheme": "data",
            "type": "image",
            "subtype": "gif",
            "encoding": "base64",
            "data": "base64data",
        },
    ),
    (
        "data:,deadbeef",
        {
            "scheme": "data",
            "data": "deadbeef",
        },
    ),
]


@pytest.mark.parametrize("data_type_string,value", data_type_data)
def test_data_type(data_type_string: str, value: dict[str, str]):
    result = Data.parse_string(data_type_string)
    resultd = result.as_dict()  # type: ignore
    assert resultd == value
