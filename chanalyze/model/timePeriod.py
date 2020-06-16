#!/usr/bin/python3

from __future__ import annotations
from typing import Tuple


class TimePeriod(object):
    def __init__(self, init: int, end: int, step: int):
        self.init = init
        self.end = end
        self.step = step

    def __contains__(self, value: int) -> bool:
        return value >= self.init and value < self.end

    def __str__(self):
        super().__str__()

        def __secondToString__(second: int) -> str:
            def __convert__(dividend: int, divisor: int) -> Tuple[int, Tuple[int, int]]:
                if divisor == 1:
                    return dividend
                else:
                    return dividend//divisor, __convert__(dividend % divisor, divisor//60)
            return '{0:02}:{1[0]:02}:{1[1]:02}'.format(*__convert__(second, 3600))

        return '{} - {}'.format(__secondToString__(self.init), __secondToString__(self.end-1))


if __name__ == '__main__':
    print('[!]This module is designed to be used as a backend handler')
    exit(0)
