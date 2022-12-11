import sys
from collections import deque


def read_instructions(filename: str) -> deque:
    instr = deque()

    with open(filename) as f:
        line = f.readline().strip()

        while line != '':
            instr.append(line.split(' '))
            line = f.readline().strip()

    return instr


class Cpu:
    def __init__(self, instructions: deque):
        self._v = 1
        self._cycle = 0
        self._signal = []
        self._instructions = instructions
        self._curr_instr = None
        self._crt_row = ''

    def run(self):
        self._register_next()

        while True:
            self._tick()
            self._update_signal()
            self._update_and_print_crt_row()

            try:
                next(self._curr_instr)
            except StopIteration:
                if len(self._instructions) == 0:
                    return self._signal

                self._register_next()

    def _cycle_to_crt_row_position(self):
        v = self._cycle % 40
        v = v if v != 0 else 40
        return v

    def _update_and_print_crt_row(self):
        curr_drawing_pos = self._cycle_to_crt_row_position()
        sprite_range = range(self._v - 1, self._v + 2)

        if curr_drawing_pos - 1 in sprite_range:
            self._crt_row += '#'
        else:
            self._crt_row += '.'

        if self._cycle % 40 == 0:
            print(self._crt_row)
            self._crt_row = ''
    
    def _tick(self):
        self._cycle += 1

    def _update_signal(self):
        if self._cycle == 20 or (self._cycle - 20) % 40 == 0:
            signal_strength = self._cycle * self._v
            self._signal.append(signal_strength)

    def _register_next(self):
        instr = self._instructions.popleft()
        self._curr_instr = self._get_instr_impl(instr)

    def _get_instr_impl(self, instr):
        if instr[0] == 'addx':
            addx_val = int(instr[1])
            return self._addx(addx_val)

        return self._noop()

    def _noop(self):
        return
        yield

    def _addx(self, v: int):
        yield
        self._v += v
    

if __name__ == '__main__':
    filename = sys.argv[1]
    instr = read_instructions(filename)
    cpu = Cpu(instructions=instr)
    signal = cpu.run()
    signal_sum = sum(signal)
    print('part1: ', signal_sum)
