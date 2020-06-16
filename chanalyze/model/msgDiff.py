#!/usr/bin/python3

from __future__ import annotations

'''
    Holds record of elapsed time between two messages sent in a Chat,
    where messages are identified using their unique `message id`

    Elapsed time will be in second ( unit )
'''


class DifferenceBetweenMessages(object):
    def __init__(self, idx1: int, idx2: int, diff: int):
        self.msgOne = idx1
        self.msgTwo = idx2
        self.elapsedTime = diff

    def __eq__(self, val: DifferenceBetweenMessages) -> bool:
        super().__eq__(val)
        return self.elapsedTime == val.elapsedTime

    def __str__(self) -> str:
        super().__str__()
        return 'Elapsed time b/w msg {} & {} -- {} s'.format(self.msgOne, self.msgTwo, self.elapsedTime)


if __name__ == '__main__':
    print('[!]This module is designed to be used as a backend handler')
    exit(0)
