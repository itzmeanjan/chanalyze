#!/usr/bin/python3

from __future__ import annotations
from functools import reduce
from unicodedata import name as getNameOfUnicodeChar
try:
    from model.chat import Chat
except Exception as e:
    print('[!]Module Unavialable : {}'.format(str(e)))
    exit(1)


def findUnicodeCharacters(chat: Chat):
    return reduce(lambda acc, cur:
                  acc +
                  reduce(lambda accInner, curInner:
                         accInner +
                         reduce(lambda accInnerDeep, curInnerDeep:
                                (accInnerDeep + [curInnerDeep]) if ord(
                                    curInnerDeep) > 255 else accInnerDeep,
                                curInner.content, []),
                         cur.messages, []),
                  chat.users, [])


if __name__ == '__main__':
    print('[!]This module is designed to be used as a backend handler')
    exit(0)
