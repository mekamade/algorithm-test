from typing import Dict


def make_km_table(pattern: str) -> Dict[str, int]:
    table = dict()
    raise Exception("TODO")
    return table


class Bm(object):
    def __init__(self, text: str, pattern: str):
        self.text = text
        self.pattern = pattern
        self.table = make_km_table(pattern)

    def decide_slide_width(self, c: str) -> int:
        assert len(c) == 1
        raise Exception("TODO")
        return -1

    def search(self) -> int:
        raise Exception("TODO")
        return -1
