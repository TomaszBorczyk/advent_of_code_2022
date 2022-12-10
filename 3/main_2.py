import sys
from main import sum_priority


def get_3_lines(f):
    return f.readline(), f.readline(), f.readline()


def search_for_duplicate(v1: str, v2: str, v3: str) -> str:
    for i in v1:
        for j in v2:
            for k in v3:
                if i == j == k:
                    return i

    return None


def process_elves(file) -> int:
    duplicates = []
    
    with open(sys.argv[1]) as f:
        while True:
            line1 = f.readline()
            line2 = f.readline()
            line3 = f.readline()

            if line1.strip() == '':
                break

            duplicate = search_for_duplicate(line1.strip(), line2.strip(), line3.strip())
            duplicates.append(duplicate)
        
    total_value = sum_priority(duplicates)

    return total_value


if __name__ == "__main__":
    v = process_elves(sys.argv[1])
    print(v)
