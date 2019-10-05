#!/usr/bin/python3

from __future__ import annotations
from datetime import datetime


class Message(object):
    def __init__(self, content: str, timeStamp: str):
        self.content = content
        self._timeStamp = timeStamp

    @property
    def timeStamp(self):
        return datetime(self._timeStamp, r'%d/%m/%y, %I:%M %p')


if __name__ == '__main__':
    print('[!]This module is designed to be used as a backend handler')
    exit(0)
