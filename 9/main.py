import sys
import dataclasses
from typing import List, Tuple, Set
import math


@dataclasses.dataclass
class Mov:
    d: str
    v: int


Coords = List[int]


def read_input(filename: str):
    movements = []

    with open(filename) as f:
        line = f.readline().strip()

        while line != '':
            args = line.split(' ')
            movements.append(Mov(d=args[0], v=int(args[1])))
            line = f.readline().strip()

    return movements


def get_distance(h_coords: Coords, t_coords: Coords) -> float:
    return math.sqrt((h_coords[0] - t_coords[0])**2 + (h_coords[1] - t_coords[1])**2)


def is_touching(h: Coords, t: Coords) -> bool:
    distance = get_distance(h, t)
    return math.floor(distance) <= 1


def get_movement_vector(h: Coords, t: Coords) -> Coords:
    def step_limiter(v: int):
        if v == 0:
            return 0
    
        normalized_step = v // abs(v)
        return normalized_step

    return (step_limiter(h[0] - t[0]), step_limiter(h[1] - t[1]))


def encode_position(coords: Coords) -> str:
    prep = [str(v) for v in list(coords)]
    return ','.join(prep)


def move(h: Coords, m: Mov) -> Coords:
    if m.d == 'U':
        h[1] += 1
    if m.d == 'D':
        h[1] -= 1
    if m.d == 'R':
        h[0] += 1
    if m.d == 'L':
        h[0] -= 1

    return h


def update_knot(h: Coords, t: Coords) -> Coords:
    if not is_touching(h, t):
        t_mov = get_movement_vector(h, t)
        t[0] += t_mov[0]
        t[1] += t_mov[1]

    return t

    
def move_all(movs: List[Mov]) -> Set[str]:
    unique_tail_positions = set()
    h = [0, 0]
    t = [0, 0]

    for m in movs:
        for _ in range(m.v):
            h = move(h, m)
            t = update_knot(h, t)
            unique_tail_positions.add(encode_position(t))

    return unique_tail_positions


def move_multi_knot(movs: List[Mov]) -> Set[str]:
    unique_tail_positions = set()
    knots = [[0, 0] for _ in range(10)]

    for m in movs:
        for _ in range(m.v):
            knots[0] = move(knots[0], m)

            for i in range(0, len(knots) - 1):
                knots[i+1] = update_knot(knots[i], knots[i+1])

            unique_tail_positions.add(encode_position(knots[len(knots) - 1]))

    return unique_tail_positions            
    

if __name__ == '__main__':
    filename = sys.argv[1]
    movs = read_input(filename)
    unique_tail_positions = move_all(movs)
    print('part1: ', len(unique_tail_positions))

    unique_tail_positions_multi = move_multi_knot(movs)
    print('part2: ', len(unique_tail_positions_multi))
