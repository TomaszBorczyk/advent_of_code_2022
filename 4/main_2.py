import sys
from functools import reduce
from main import parse_file, overlap_count, PairSections


def do_sections_overlap(s: PairSections) -> bool:
    s1 = s[0]
    s2 = s[1]

    if s2[0] <= s1[1] and s2[0] >= s1[0]:
        return True

    if s1[0] >= s2[0] and s1[0] <= s2[1]:
        return True

    return False


if __name__ == '__main__':
    sections = parse_file(sys.argv[1])
    overlapping = reduce(lambda x, y: x + overlap_count(do_sections_overlap(y)), sections, 0)
    print(overlapping)
