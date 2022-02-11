from typing import Dict


def make_km_table(pattern: str) -> Dict[str, int]:
    table = dict()
    pattern_length = len(pattern)
    table["*"] = pattern_length
    for index, char in enumerate(pattern):
        value = max(1, pattern_length-index-1)
        table[char] = value
    return table


class Bm(object):
    def __init__(self, text: str, pattern: str):
        self.text = text
        self.pattern = pattern
        self.table = make_km_table(pattern)

    def decide_slide_width(self, c: str) -> int:
        assert len(c) == 1
        slide_width = self.table[c] if c in self.table else self.table["*"]
        return slide_width

    def search(self) -> int:
        text_length = len(self.text)
        pattern_length = len(self.pattern)
        assert pattern_length <= text_length
        text_ptr = pattern_length - 1
        while text_ptr < text_length:
            for i in range(pattern_length):
                if self.text[text_ptr-i] != self.pattern[-1-i]:
                    slide_width = self.decide_slide_width(self.text[text_ptr-i])
                    text_ptr += slide_width
                    break
                if i == pattern_length - 1:
                    return text_ptr - i
        return -1
