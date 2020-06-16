#!/usr/bin/python3

from __future__ import annotations
from datetime import datetime
from math import ceil

'''
    Used for holding all messages for
    a certain chat ( for both group & private )
'''


class Message(object):
    def __init__(self, index: int, content: str, timeStamp: str):
        self.index = index
        self.content = content.rstrip()
        self._timeStamp = timeStamp

    '''
        Returns timestamp of a message as a datetime
        object ( parsed from string timestamp )
    '''
    @property
    def timeStamp(self) -> datetime:
        try:
            return datetime.strptime(self._timeStamp, r'%d/%m/%y, %I:%M %p')
        except ValueError:
            return datetime.strptime(self._timeStamp, r'%d/%m/%Y, %I:%M %p')

    def __str__(self):
        super().__str__()
        return '{} - {}***... - {}'.format(self.index, self.content[:ceil(len(self.content)/9)], str(self.timeStamp))


'''
    A temporary class, used for keeping track of message indices,
    while parsing Chat from text file
'''


class MessageIndex(object):
    def __init__(self, idx: int):
        self.index = idx

    def increment(self, by: int = 1):
        self.index += by


if __name__ == '__main__':
    print('[!]This module is designed to be used as a backend handler')
    exit(0)
