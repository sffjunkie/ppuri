from ppuri.component import fragment


def test_fragment():
    result = fragment.parse("#afragmemt")
    assert result == "afragmemt"
