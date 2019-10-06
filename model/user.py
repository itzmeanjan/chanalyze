#!/usr/bin/python3

from __future__ import annotations
from typing import List
try:
    from message import Message
except ImportError as e:
    print('[!]Module Unavailable : {}'.format(str(e)))
    exit(1)

'''
    Holds all messages sent by a certain user, participated in a chat
    ( for both private & group ), along with its name
'''


class User(object):
    def __init__(self, name: str, messages: List[Message]):
        self.name = name
        self.messages = messages


if __name__ == '__main__':
    print('[!]This module is designed to be used as a backend handler')
    exit(0)
