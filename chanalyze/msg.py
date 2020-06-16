#!/usr/bin/python3

from __future__ import annotations
from functools import reduce
from collections import Counter
from math import floor

from .model.chat import Chat

def analyze(chat: Chat):
    return removeSpecialCharacters(Counter(
        reduce(lambda acc, cur:
               acc + reduce(lambda accInner,
                            curInner: accInner + curInner.content.split(), cur.messages, []),
               chat.users, [])))


def isASCIISpecialCharacter(c: str) -> bool:
    # here I'm trying to determine whether this is an ASCII special char or not
    return True if len(c) == 1 and (0 <= ord(c) <= 255) and not (96 < ord(c) < 123) and not (64 < ord(c) < 91) else False


def getMedian(frm: int, to: int) -> int:
    return floor((frm + to)/2)


def removeSpecialCharacters(words: Counter) -> Counter:
    # removing all those keys, which are having any combination of only ASCII special characters
    for i in list(words.keys()):
        if all(map(isASCIISpecialCharacter, i)):
            words.pop(i)
    medianV = getMedian(min(words.values()), max(words.values()))
    # removing all those keys from dictionary, which are having value lesser than median
    for i in list(words.keys()):
        if words[i] < medianV:
            words.pop(i)
    return words


if __name__ == '__main__':
    print('[!]This module is designed to be working as a backend handler')
    exit(0)
