import pytest

# import pyparsing as pp

from ppuri.component.userinfo import UserInfo, userinfo_scan

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
    res = UserInfo.parse_string(text, parse_all=True).as_dict()  # type: ignore
    assert res["username"] == info["username"]
    assert res["password"] == info["password"]


@pytest.mark.parametrize("text,info", userinfo_scan_text)
def test_userinfo_scan(text: str, info: list[dict[str, str]]):
    res = userinfo_scan(text)  # type: ignore
    assert len(res) == len(info)
    assert res[0]["username"] == info[0]["username"]
