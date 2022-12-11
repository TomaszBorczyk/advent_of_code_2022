import sys
import math
import dataclasses
from typing import List, Callable
from collections import deque


Worry = int
Divisor = int
MonkeyId = int
TestProcedure = Callable[[Worry], bool]


@dataclasses.dataclass
class Monkey:
    id: int
    items: deque
    operation: Callable[[Worry], Worry]
    test_val: int
    tru_target: MonkeyId
    fals_target: MonkeyId
    insp_count: int = 0


def parse_operation(line: str):
    op_str = line.split(" = ")[1]
    args = op_str.split(" ")
    op_type = args[1]

    if args[2].isnumeric():
        param = int(args[2])
        if op_type == '+':
            return lambda x: x + param
        if op_type == '*':
            return lambda x: x * param
    else:
        return lambda x: x * x
        

def read_monkey(f, id) -> Monkey:
    line = f.readline().strip()
    
    while line != '':
        if 'Starting items' in line:
            items_str = line.split(': ')[1]
            items = [int(v) for v in items_str.split(',')]
            items = deque(items)

        if 'Operation:' in line:
            operation = parse_operation(line)

        if 'Test:' in line:
            divisor = int(line.split('by ')[1])

        if 'If true' in line:
            tru_target = int(line.split('monkey ')[1])

        if 'If false' in line:
            fals_target = int(line.split('monkey ')[1])

        line = f.readline().strip()

    return Monkey(
        id=id,
        items=items,
        operation=operation,
        test_val=divisor,
        tru_target=tru_target,
        fals_target=fals_target
    ) 
            

def read_monkeys(filename: str):
    monkeys = []

    with open(filename) as f:
        mode = 'M' # M - look for monkey, P - process monkey

        empty_line_count = 0

        while True:
            if mode == 'M':
                line = f.readline().strip()

                if 'Monkey ' in line:
                    mode = 'P'
                    empty_line_count = 0
                else:
                    empty_line_count += 1

                if empty_line_count > 1: # eof detected
                    return monkeys

            if mode == 'P':
                id = int(line[:-1].split(' ')[1])
                m = read_monkey(f, id)
                monkeys.append(m)
                mode = 'M'


def play(monkeys: List[Monkey], rounds: int, lcm: int, worry_divisor: int):
    for _ in range(rounds):
        for m in monkeys:
            while len(m.items) > 0:
                i = m.items.popleft()
                w = m.operation(i)
                w = w // worry_divisor
                w = w % lcm
                decision = w % m.test_val == 0
                target = m.tru_target if decision else m.fals_target
                monkeys[target].items.append(w)
                m.insp_count += 1


def get_monkey_business(monkeys: List[Monkey]) -> int:
    s = sorted(monkeys, key=lambda x: x.insp_count, reverse=True)
    return s[0].insp_count * s[1].insp_count


if __name__ == '__main__':
    filename = sys.argv[1]

    # part 1
    monkeys = read_monkeys(filename)
    divisors = [m.test_val for m in monkeys]
    lcm = math.lcm(*divisors)
    play(monkeys, 20, lcm, 3)        
    mb = get_monkey_business(monkeys)
    print('part1: ', mb)

    # part2 
    monkeys = read_monkeys(filename)
    play(monkeys, 10000, lcm, 1)        
    mb = get_monkey_business(monkeys)
    print('part2: ', mb)
