from ppuri.component import path


def test_path_empty():
    _result = path.Path("")
    pass


def test_path():
    results = path.parse("/file.txt")
    assert results == "/file.txt"
