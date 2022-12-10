import sys
from collections import deque


def get_input(filename: str) -> str:
    with open(filename) as f:
        return f.readline()


def is_unique(chars: deque):
    return len(set(chars)) == len(chars)
    

def find_marker(data: str, max_chars: int) -> int:
    last_chars = deque(maxlen=max_chars)
    
    for i, char in enumerate(data):
        last_chars.append(char)

        if len(last_chars) == last_chars.maxlen and is_unique(last_chars):
            return i + 1

    return -1
    

if __name__ == "__main__":
    input_filename = sys.argv[1]
    input = get_input(input_filename)
    marker = find_marker(input, 4)
    marker2 = find_marker(input, 14)
    print(marker, marker2)
