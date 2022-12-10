from __future__ import annotations
import sys
from dataclasses import dataclass, field
from typing import List


def get_input(filename: str):
    return open(filename)


@dataclass
class Fil:
    name: str
    size: int


class Dir:
    def __init__(self, name: str, parent: Dir = None):
        self.name = name
        self.dirs: List[Dir] = []
        self.files: List[Fil] = []
        self.size: int = 0
        self.parent = parent

    def add_file(self, fil: Fil):
        self.files.append(fil)
        self._update_size(fil.size)

    def add_dir(self, d: Dir):
        self.dirs.append(d)

    def _update_size(self, size: int):
        self.size += size

        if self.parent:
            self.parent._update_size(size)

    def __repr__(self):
        return f'{self.name}: {self.size}'
            

class Parser:
    def __init__(self, data, start_dir):
        self.current_dir = start_dir
        self.data = data
        self.current_line = None

    def parse(self):
        self._read_next_line()

        while self.current_line != '':
            if self._is_command(self.current_line):
                self._execute_command(self.current_line)

    def _is_command(self, text: str) -> bool:
        return text.startswith('$')

    def _execute_command(self, command: str):
        args = command.split(' ')

        if args[1] == 'cd':
            if args[2] == '..':
                self._go_up()
            elif args[2] == '/':
                pass
            else:
                self._go_to_child_dir(dirname=args[2])

            self._read_next_line()

        if args[1] == 'ls':
            self._process_list()

    def _read_next_line(self):
        self.current_line = self.data.readline().strip()

    def _go_up(self):
        self.current_dir = self.current_dir.parent
        
    def _go_to_child_dir(self, dirname: str):
        child_dir = next(x for x in self.current_dir.dirs if x.name == dirname)
        self.current_dir = child_dir

    def _process_list(self):
        self._read_next_line()

        while not self._is_command(self.current_line) and self.current_line != '':
            args = self.current_line.split(' ')

            if args[0] == 'dir':
                new_dir = Dir(name=args[1], parent=self.current_dir)
                self.current_dir.add_dir(new_dir)
            else:
                new_file = Fil(name=args[1], size=int(args[0]))
                self.current_dir.add_file(new_file)

            self._read_next_line()


class Traversal:
    def __init__(self, start_dir: Dir, condition: Callable[[Dir], bool]):
        self.current_dir = start_dir
        self.valid_dirs = []
        self.condition = condition

    def get_valid_dirs(self) -> List[Dir]:
        self._traverse(self.current_dir)
        return self.valid_dirs

    def _traverse(self, cur_dir: Dir):
        if self.condition(cur_dir):
            self.valid_dirs.append(cur_dir)

        for d in cur_dir.dirs:
            self._traverse(d)
    

if __name__ == "__main__":
    input_filename = sys.argv[1]
    input = get_input(input_filename)

    start_dir = Dir(name='/')

    parser = Parser(input, start_dir)
    parser.parse()

    trav = Traversal(start_dir=start_dir, condition = lambda d: d.size < 100000)
    valid_dirs = trav.get_valid_dirs()
    total_size = sum([dir.size for dir in valid_dirs])
    print('part1: ', total_size)

    total_sys_size = 70000000
    needed_free = 30000000
    taken_size = start_dir.size
    free_size = total_sys_size - taken_size
    needed_for_cleanup = needed_free - free_size
    
    trav2 = Traversal(start_dir=start_dir, condition = lambda d: d.size > needed_for_cleanup)
    potential_deletion_dirs = trav2.get_valid_dirs()
    potential_sorted = sorted(potential_deletion_dirs, key=lambda x: x.size)
    
    smallest_valid_deletion = potential_sorted[0]
    print('part2: ', smallest_valid_deletion.size)
