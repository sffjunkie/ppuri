from ppuri.component.path import Path


def test_path_empty():
    _result = Path("")
    pass


def test_path_ends_with_space():
    results = Path.parse_string("/file.txt as")
    assert results[0] == "/file.txt"
