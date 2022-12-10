import sys
import re
import dataclasses

from typing import List


@dataclasses.dataclass
class Movement:
    amount: int
    source: int
    dest: int


def pad_crates(line: str) -> str:
    parsed = line.replace('     ', ' [ ] ')
    parsed = parsed.replace('    ', '[ ] ')
    parsed = parsed.replace('  ', ' ')
    parsed = parsed.replace('][', '] [')
    return parsed


def parse_movement(line: str) -> Movement:
    matches = list(re.finditer('([0-9])*([0-9])*([0-9])', line))

    return Movement(
        amount=int(matches[0].group()),
        source=int(matches[1].group()),
        dest=int(matches[2].group())
    )


def parse_crates(line: str) -> List[str]:
    matches = list(re.finditer(r"\[([A-Z\s])\]", line))
    return [v.group(1) if v.group(1) != ' ' else None for v in matches]



def parse_input(filename: str):
    crates = []
    movements = []

    with open(filename) as f:
        # process crates
        while True:
            line = f.readline()

            if line.strip() == '':
                break
            
            if '[' in line:
                padded_crate_line = pad_crates(line)
                # print(padded_crate_line)
                elems = parse_crates(padded_crate_line)

                if len(crates) == 0:
                    crates = [[] for i in range(len(elems))]

                for i, elem in enumerate(elems):
                    if elem is not None:
                        crates[i].insert(0, elem)

        # process commands
        while True:
            line = f.readline()
            
            if line.strip() == '':
                break
            
            if 'move' in line:
                mv = parse_movement(line.strip())
                movements.append(mv)

    return crates, movements


def execute_movement(crates: List[List[str]], mv: Movement) -> List[List[str]]:
    reps = mv.amount

    while reps > 0:
        c = crates[mv.source - 1].pop()
        crates[mv.dest - 1].append(c)
        reps -= 1

    return crates


def execute_movement_2(crates: List[List[str]], mv: Movement) -> List[List[str]]:
    reps = mv.amount

    if reps == 1:
        c = crates[mv.source - 1].pop()
        crates[mv.dest - 1].append(c)
    else:
        c = crates[mv.source - 1][-reps:]
        crates[mv.source - 1] = crates[mv.source - 1][:-reps]
        crates[mv.dest - 1].extend(c)

    return crates


if __name__ == '__main__':
    crates, movements = parse_input(sys.argv[1])

    for i, mv in enumerate(movements):
        print(i)
        execute_movement_2(crates, mv)

    top_crates = [column[-1] for column in crates]
    res = ''.join(top_crates)

    print(res)

