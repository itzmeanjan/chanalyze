#!/usr/bin/python3

from __future__ import annotations
from datetime import datetime

'''
    Used for holding all messages for 
    a certain chat ( for both group & private )
'''


class Message(object):
    def __init__(self, content: str, timeStamp: str):
        self.content = content.rstrip()
        self._timeStamp = timeStamp

    '''
        Returns timestamp of a message as a datetime 
        object ( parsed from string timestamp )
    '''
    @property
    def timeStamp(self) -> datetime:
        return datetime.strptime(self._timeStamp, r'%d/%m/%y, %I:%M %p')


if __name__ == '__main__':
    print('[!]This module is designed to be used as a backend handler')
    exit(0)
