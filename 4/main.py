import sys
from typing import List
from functools import reduce


Section = List[int]
PairSections = List[Section]


def get_section_range(encoded_range: str) -> Section:
    return [int(s) for s in encoded_range.split('-')]


def parse_line(line: str) -> List[int]:
    pair: List[str] = line.split(',')
    sections1 = get_section_range(pair[0])
    sections2 = get_section_range(pair[1])

    return [sections1, sections2]


def do_sections_overlap(s: PairSections) -> bool:
    s1 = s[0]
    s2 = s[1]

    if s1[0] >= s2[0] and s1[1] <= s2[1]:
        return True

    if s1[0] <= s2[0] and s1[1] >= s2[1]:
        return True

    return False


def overlap_count(is_overlapping: bool) -> int:
    return 1 if is_overlapping else 0


def parse_file(filename: str):
    sections = []

    with open(filename) as f:
        while True:
            line = f.readline().strip()

            if line == '':
                break
            
            pair_sections = parse_line(line)
            sections.append(pair_sections)

    return sections


if __name__ == "__main__":
    sections = parse_file(sys.argv[1])
    overlapping = reduce(lambda x, y: x + overlap_count(do_sections_overlap(y)), sections, 0)
    print(overlapping)

    
