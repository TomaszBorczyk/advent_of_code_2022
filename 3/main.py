import sys
from typing import List
from functools import reduce


def read_data(filename: str):
    f = open(filename)
    return f


ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
UPPERCASE_ADDITIONAL_VALUE = len(ALPHABET)


def get_character_value(char: str) -> int:
    base_value = 1 + ALPHABET.index(char.lower())

    if char.isupper():
        return base_value + UPPERCASE_ADDITIONAL_VALUE

    return base_value


def search_for_duplicate(rucksack: str) -> str:
    capacity = len(rucksack)
    #h1 = rucksack[0:capacity//2]
    #h2 = rucksack[capacity//2:capacity]
    #print(rucksack, len(rucksack), h1, len(h1), h2, len(h2))

    for i in range(0, capacity//2):
        c1 = rucksack[i]
        
        for j in range(capacity//2, capacity):
            c2 = rucksack[j]

            if c1 == c2:
                return c1

    return None


def get_all_duplicates(filename: str):
    data = read_data(filename)
    duplicates = []

    for rucksack in data:
        duplicate = search_for_duplicate(rucksack.strip())
        duplicates.append(duplicate)

    return duplicates


def sum_priority(items: List[str]) -> int:
    return reduce(lambda x, y: x + get_character_value(y), items, 0)


if __name__ == '__main__':
    duplicates = get_all_duplicates(sys.argv[1])
    print(duplicates)
    total_value = sum_priority(duplicates)
    print(total_value)
