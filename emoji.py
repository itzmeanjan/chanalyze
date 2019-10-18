#!/usr/bin/python3

from __future__ import annotations
from functools import reduce
from unicodedata import name as getNameOfUnicodeChar
from typing import List
from collections import Counter
try:
    from model.chat import Chat
except Exception as e:
    print('[!]Module Unavialable : {}'.format(str(e)))
    exit(1)

'''
    Extracts all those non-ascii characters
    from Chat, which are to be filtered further,
    so that we can keep only those unicode characters,
    which are emojis.

    And understand emoji usage of this Chat
'''


def findNonASCIICharactersinText(chat: Chat) -> List[str]:
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


'''
    Filters out only those unicode characters,
    which are emojis, from a list of all 
    non-ascii characters used in this Chat,
    using a list of integers, which is nothing but
    all supported emojis numeric representation
'''


def findEmojisInText(data: List[str], emojiData: List[int]) -> List[str]:
    return reduce(lambda acc, cur:
                  acc + [cur] if ord(cur) in emojiData else acc,
                  data, [])


'''
    Returns a statistics of which emojis was used how many
    times in a certain Chat ( which is currently under consideration ),
    from a list of all used emojis in this Chat
'''


def findEmojiUsage(emojis: List[str]) -> Counter:
    return Counter(emojis)


if __name__ == '__main__':
    print('[!]This module is designed to be used as a backend handler')
    exit(0)
