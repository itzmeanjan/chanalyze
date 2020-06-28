#!/usr/bin/python3

from __future__ import annotations
from functools import reduce
from unicodedata import name as getNameOfUnicodeChar
from typing import List
from collections import Counter
from matplotlib.colors import cnames
from matplotlib import pyplot as plt
import ray

from .model.chat import Chat

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


@ray.remote
def plotEmojiUsage(emojis: Counter, targetPath: str, title: str, top: int = 7) -> bool:
    try:
        _tmpLabels = reduce(lambda acc, cur: acc + [cur] if len(acc) < (top+1) else acc, sorted(
            emojis, key=lambda e: emojis[e], reverse=True), [])
        total = sum([emojis[i] for i in emojis])
        _remaining = total - sum([emojis[i] for i in _tmpLabels])
        data = [emojis[i] for i in _tmpLabels] + \
            [_remaining] if len(_tmpLabels) < len(emojis) else []
        labels = ['{} ( {:7.4f} % )'.format(getNameOfUnicodeChar(i).title(), emojis[i]*100/total)
                  for i in _tmpLabels] + \
            ['Others ( {:7.4f} % )'.format(_remaining*100/total)] if len(
                _tmpLabels) < len(emojis) else []
        font = {
            'family': 'serif',
            'color': '#000000',
            'weight': 'normal',
            'size': 16
        }
        plt.figure(figsize=(24, 12), dpi=100)
        patches, _ = plt.pie(data)
        plt.legend(patches, labels, loc='best', fontsize='large')
        plt.title(title, fontdict=font)
        plt.axis('equal')
        plt.tight_layout()
        plt.savefig(targetPath, bbox_inches='tight',
                    pad_inches=.6, quality=95, dpi=100)  # exporting plotted PIE chart
        plt.close()  # closing this figure on which we just plotted a PIE chart
        return True
    except Exception:
        return False


if __name__ == '__main__':
    print('[!]This module is designed to be used as a backend handler')
    exit(0)
