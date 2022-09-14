import pytest

# import pyparsing as pp

from ppuri.component import userinfo

userinfo_test_data: list[tuple[str, dict[str, str]]] = [
    ("user:pass", {"username": "user", "password": "pass"}),
    ("user:pass@", {"username": "user", "password": "pass"}),
    ("user:", {"username": "user", "password": ""}),
    ("user:@", {"username": "user", "password": ""}),
]

userinfo_scan_text = [
    (
        "User information = user:pass@somewhere",
        [{"username": "user", "password": "pass"}],
    ),
    (
        "User information = user:pass somewhere and anotheruser:password",
        [
            {"username": "user", "password": "pass"},
            {"username": "anotheruser", "password": "password"},
        ],
    ),
]


@pytest.mark.parametrize("text,info", userinfo_test_data)
def test_userinfo_parse(text: str, info: dict[str, str]):
    res = userinfo.parse(text)  # type: ignore
    assert res["username"] == info["username"]
    assert res["password"] == info["password"]
