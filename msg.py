#!/usr/bin/python3

from __future__ import annotations
from functools import reduce
from collections import Counter
try:
    from model.chat import Chat
except ImportError as e:
    print('[!]Module Unavailable : {}'.format(str(e)))
    exit(1)


def analyze(chat: Chat):
    return removeSpecialCharacters(Counter(
        reduce(lambda acc, cur:
               acc + reduce(lambda accInner,
                            curInner: accInner + curInner.content.split(), cur.messages, []),
               chat.users, [])))


def removeSpecialCharacters(words: Counter) -> Counter:
    keys = list(words.keys())
    for i in keys:
        # here I'm trying to determine whether current key is one of ASCII special keywords or not
        if len(i) == 1 and (0 <= ord(i) <= 255) and not (96 < ord(i) < 123) and not (64 < ord(i) < 91):
            words.pop(i)
    return words


if __name__ == '__main__':
    print('[!]This module is designed to be working as a backend handler')
    exit(0)
