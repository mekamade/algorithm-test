from typing import Dict
import logging

logger = logging.getLogger()


def make_bad_match_table(pattern: str) -> Dict[str, int]:
    logger.info("Generating Bad Match Table...")
    table = dict()
    pattern_length = len(pattern)
    for index, char in enumerate(pattern[:-1]):
        value = max(1, pattern_length-index-1)
        table[char] = value
        logger.info(f"\t- For character: '{char}' [{index}], set value: {value}")
    if pattern:
        last_char = pattern[-1]
        if last_char in table:
            logger.info(f"\t- Ignoring last character: '{last_char}', "
                        "as it is already registered in table")
        else:
            table[last_char] = pattern_length
            logger.info(f"\t- For last character: '{last_char}', "
                        f"set value as pattern length: {pattern_length}")
    table["*"] = pattern_length
    logger.info(f"\t- For all other characters (*), "
                f"set value as pattern length: {pattern_length}")
    logger.info(f"Generated Bad Match Table: {table}")
    return table

def make_good_suffix_table(pattern: str) -> Dict[int, int]:
    table = dict()
    logger.info("Generating Good Suffix Table...")
    pattern_length = len(pattern)
    for suffix_length in range(1, pattern_length):
        found_whole_suffix, found_partial_suffix = False, False
        suffix = pattern[-suffix_length:]
        logger.info(f"\t- Current Target Suffix: {suffix} [Length: {len(suffix)}]")
        suffix_start_index = pattern_length-suffix_length
        for i in range(suffix_start_index-suffix_length+1):
            test_start_index = suffix_start_index-suffix_length-i
            test_stop_index = suffix_start_index-i
            test_suffix = pattern[test_start_index:test_stop_index]
            shift_distance = suffix_start_index - test_start_index
            if suffix == test_suffix:
                logger.info(f"\t\t- Test Suffix: {test_suffix} "
                            f"[{test_start_index}-{test_stop_index-1}] "
                            "(Match: OK)")
                suffix_predecessor_index = suffix_start_index-1
                suffix_predecessor = pattern[suffix_predecessor_index]
                test_predecessor_index = test_start_index-1
                if test_predecessor_index < 0:
                    table[suffix_length] = shift_distance
                    found_whole_suffix = True
                    logger.info(f"\t\t\t- Unique Prefixes: '<empty>' != "
                                f"'{suffix_predecessor}' [{suffix_predecessor_index}] "
                                f"(Match: OK ✅) Set Value: {shift_distance}")
                    break
                test_predecessor = pattern[test_predecessor_index]
                if test_predecessor != suffix_predecessor:
                    table[suffix_length] = shift_distance
                    found_whole_suffix = True
                    logger.info(f"\t\t\t- Unique Prefixes: '{test_predecessor}' "
                                f"[{test_predecessor_index}] != '{suffix_predecessor}' "
                                f"[{suffix_predecessor_index}] (Match: OK ✅) "
                                f"Set Value: {shift_distance}")
                    break
                else:
                    logger.info(f"\t\t\t- Prefix Matched: '{test_predecessor}' "
                                f"[{test_predecessor_index}] == '{suffix_predecessor}' "
                                f"[{suffix_predecessor_index}] (Match: IGNORED ❌)")
                    continue
            else:
                logger.debug(f"\t\t- Test Suffix: {test_suffix} "
                        f"[{test_start_index}-{test_stop_index-1}] "
                        "(Match: NO ❌)")
        if not found_whole_suffix:
            for i in range(suffix_length-1):
                partial_suffix_length = suffix_length-i-1
                partial_suffix = pattern[:partial_suffix_length]
                if suffix[-partial_suffix_length:] == partial_suffix:
                    table[suffix_length] = pattern_length-partial_suffix_length
                    logger.info(f"\t\t- Partial Test Suffix: {partial_suffix} "
                                f"Corresponding Target Suffix: {suffix[-partial_suffix_length:]} "
                                f"(Match: OK ✅) Set Value: {pattern_length-partial_suffix_length}")
                    found_partial_suffix = True
                    break
                else:
                    logger.debug(f"\t\t- Partial Test Suffix: {partial_suffix} "
                                f"Corresponding Target Suffix: {suffix[-partial_suffix_length:]} "
                                "(Match: NO ❌)")
        if not found_partial_suffix and not found_whole_suffix:
            table[suffix_length] = pattern_length
            logger.info(f"\t\t- No matching suffix found, "
                        f"set value as pattern length: {pattern_length}")
    table[0] = 1
    logger.info(f"Generated Good Suffix Table: {table}")
    return table


class Bm(object):
    def __init__(self, text: str, pattern: str):
        self.text = text
        self.pattern = pattern
        logger.info(f"Preprocessing Pattern: {pattern}")
        logger.info("***")
        self.bm_table = make_bad_match_table(pattern)
        logger.info("***")
        self.gs_table = make_good_suffix_table(pattern)

    def decide_slide_width(self, char: str, matched_count: int) -> int:
        assert len(char) == 1
        bm_table_query = self.bm_table[char] if char in self.bm_table else self.bm_table["*"]
        bm_slide_width = max(1, bm_table_query - matched_count)
        gs_slide_width = self.gs_table[matched_count]
        best_slide_width = max(bm_slide_width, gs_slide_width)
        return best_slide_width

    def search(self) -> int:
        logger.info("***")
        logger.info(f"Searching for '{self.pattern}' in '{self.text}'...")
        text_length = len(self.text)
        pattern_length = len(self.pattern)
        if pattern_length == 0 or text_length < pattern_length:
            logger.info(f"Pattern not found in text!")
            return -1
        text_ptr = pattern_length - 1
        while text_ptr < text_length:
            for i in range(pattern_length):
                if self.text[text_ptr-i] != self.pattern[-1-i]:
                    slide_width = self.decide_slide_width(self.text[text_ptr-i], i)
                    text_ptr += slide_width
                    logger.info(f"\t- Made a jump of {slide_width} places")
                    break
                if i == pattern_length - 1:
                    logger.info(f"Pattern: '{self.pattern}' located in "
                                f"'{self.text}' at index: {text_ptr-i}")
                    return text_ptr - i
        logger.info(f"Pattern not found in text!")
        return -1