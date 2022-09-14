from ppuri.component.fragment import Fragment


def test_fragment():
    res = Fragment.parse_string("#afragmemt")
    res_d = res.as_dict()  # type: ignore
    assert res_d["fragment"] == "afragmemt"
