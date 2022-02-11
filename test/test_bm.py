import pytest

from src.bm import Bm

@pytest.mark.parametrize("text,pattern,expected", [
    ("GCTCACTGAGCGCTCGT", "GCTCG", 11),
    ("GCTCACTGAGCGCTCGT", "CACTGAG", 3),
    ("GCTCACTGAGCGCTCGT", "AAAAA", -1),
    ("GCTCACTGAGCGCTCGT", "GCTCGTT", -1),
    ("GCTCACTGAGCGCTCGT", "GCTCACTGAGCGCTCGT", 0),
    ("ANPANMAN", "PAN", 2),
    ("ANPANMAN", "ANPAN", 0),
    ("ANPANMAN", "BIKINMAN", -1),
])
def test_bm(text, pattern, expected):
    bm = Bm(text, pattern)

    actual = bm.search()

    assert actual == expected
    # assert False  # for print debugging
