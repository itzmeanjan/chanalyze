#!/usr/bin/python3

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
    def __init__(self, name: str, messages):
        self.name = name
        self.messages = messages

    def __str__(self):
        super().__str__()
        return '{} with {} messages'.format(self.name, len(self.messages))


if __name__ == '__main__':
    print('[!]This module is designed to be used as a backend handler')
    exit(0)
