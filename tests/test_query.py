import pytest
from ppuri.component.query import param, QueryParams, Query

good_param = [
    ("q=2", {"name": "q", "value": "2"}),
    ("p", {"name": "p", "value": None}),
]

good_param_list = [
    ("p=2&q=3", [{"name": "p", "value": "2"}, {"name": "q", "value": "3"}]),
    ("p=2&q", [{"name": "p", "value": "2"}, {"name": "q", "value": None}]),
]

good_queries = [
    ("?param", [{"name": "param", "value": None}]),
    ("?param=2", [{"name": "param", "value": "2"}]),
    (
        "?param1=2&param2=wibble",
        [{"name": "param1", "value": "2"}, {"name": "param2", "value": "wibble"}],
    ),
    (
        "?param1=2&param2=wibble&param3",
        [
            {"name": "param1", "value": "2"},
            {"name": "param2", "value": "wibble"},
            {"name": "param3", "value": None},
        ],
    ),
]


@pytest.mark.parametrize("param_string,result", good_param)
def test_query_param(param_string: str, result: dict[str, str | None]):
    res = param.parse_string(param_string)
    parameter = res[0].as_dict()  # type: ignore
    assert parameter["name"] == result["name"]
    assert parameter["value"] == result["value"]


@pytest.mark.parametrize("param_list_string,result", good_param_list)
def test_query_param_list(param_list_string: str, result: dict[str, str | None]):
    res = QueryParams.parse_string(param_list_string)
    res_dict = res.as_dict()  # type: ignore
    parameters = res_dict["parameters"]  # type: ignore
    assert parameters == result


@pytest.mark.parametrize("query_string,params", good_queries)
def test_query_parse_good(query_string: str, params: list[str]):
    res = Query.parse_string(query_string)  # type: ignore
    d = res.as_dict()  # type: ignore
    parameters = d["parameters"]  # type: ignore
    assert params == parameters
