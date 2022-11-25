from typing import Optional, NoReturn, List, TypeVar

T = TypeVar('T')

class NanoIter:
    def __init__(self, l: List[T]):
        self.i = -1
        self.l: List[T] = l

    def next(self) -> T:
        if self.i == len(self.l):
            raise StopIteration()
        else:
            self.i += 1
            return self.l[self.i]

    def get(self, i = None):
        return self.l[self.i] if not i else self.l[i]

    def back(self) -> NoReturn:
        if self.i <= 0:
            self.i = -1
        else:
            self.i -= 1

    def peek(self) -> T:
        if self.i == len(self.l):
            raise StopIteration()
        else:
            return self.l[self.i + 1]
