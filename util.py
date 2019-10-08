#!/usr/bin/python3

from __future__ import annotations
from os.path import abspath, dirname, exists
from os import mkdir
from functools import reduce
from typing import Dict, List
from collections import OrderedDict
from math import ceil
try:
    from matplotlib import pyplot as plt
    from matplotlib.ticker import MultipleLocator, PercentFormatter
    from model.chat import Chat
    from model.user import User
    from model.message import Message
    from model.timePeriod import TimePeriod
except ImportError as e:
    print('[!]Module Unavailable : {}'.format(str(e)))
    exit(1)


# checks whether directory of this path already exists or not.
# if not, creates that directory
def directoryBuilder(targetPath: str):
    dirName = dirname(abspath(targetPath))
    if not exists(dirName):
        mkdir(dirName)


# shades first half of characters of Contact by `*`, for sake of privacy
def shadeContactName(name: str, percent: float = 50.0, where: str = 'f') -> str:
    return '*'*ceil(len(name)*percent/100) + name[ceil(len(name)*percent/100):] if where.lower() == 'f' else name[:-ceil(len(name)*percent/100)] + '*'*ceil(len(name)*percent/100)


'''
    How a certain person contributed to a Chat between two persons ( Private )
    or more ( Group ), is plotted into a Bar Chart ( shows contribution in percentage )
'''


def plotContributionInChatByUser(chat: Chat, targetPath: str, title: str) -> bool:
    try:
        directoryBuilder(targetPath)
        y = sorted([i.name for i in chat.users],
                   key=lambda e: len(chat.getUser(e).messages))
        y_pos = range(len(y))
        x = [len(chat.getUser(i).messages)/chat.messageCount*100 for i in y]
        y = [shadeContactName(i, percent=75) for i in y]
        with plt.style.context('ggplot'):
            font = {
                'family': 'serif',
                'color': '#000000',
                'weight': 'normal',
                'size': 14
            }
            plt.figure(figsize=(24, 12), dpi=100)
            plt.xlim((0, 100))
            plt.gca().xaxis.set_major_locator(MultipleLocator(10))
            plt.gca().xaxis.set_major_formatter(PercentFormatter())
            plt.gca().xaxis.set_minor_locator(MultipleLocator(1))
            plt.barh(y_pos, x, align='center',
                     color='steelblue', lw=1.6)
            plt.gca().yaxis.set_ticks(y_pos)
            plt.gca().yaxis.set_ticklabels(y)
            plt.xlabel('Percentage of Participation in Chat',
                       fontdict=font, labelpad=16)
            plt.title(title,
                      fontdict=font, pad=16)
            plt.tight_layout()
            plt.savefig(targetPath, bbox_inches='tight', pad_inches=.5)
            plt.close()
        return True
    except Exception:
        return False


def plotContributionOfUserByHour(messages: List[Message], targetPath: str, title: str) -> bool:

    def __buildStatusHolder__(holder: Dict[str, int], current: Message) -> Dict[str, int]:
        tm = current.timeStamp.timetz()
        seconds = tm.hour*3600 + tm.minute*60
        found = str(
            reduce(lambda acc, cur: cur if seconds in cur else acc, ranges, None))
        holder.update({found: holder.get(found, 0)+1})
        return holder

    try:
        directoryBuilder(targetPath)
        ranges = [TimePeriod(i, i+3600*3, 1)
                  for i in range(0, 86400, 3600*3)]
        splitted = reduce(__buildStatusHolder__, messages,
                          dict([(str(i), 0) for i in ranges]))
        _tmpLabels = sorted(splitted)
        data = [splitted[i] for i in _tmpLabels]
        splitted = OrderedDict([(i, splitted[i])
                                for i in _tmpLabels])
        _tmpLabels = [i for i in splitted]
        data = [splitted[i] for i in _tmpLabels]
        total = sum(data)
        labels = ['{} ( {:7.4f} % )'.format(i, splitted[i]*100/total)
                  for i in _tmpLabels]
        font = {
            'family': 'serif',
            'color': '#000000',
            'weight': 'normal',
            'size': 16
        }
        plt.figure(figsize=(24, 12), dpi=100)
        patches, _ = plt.pie(data)  # plotting pie chart
        plt.legend(patches, labels, loc='best', fontsize='medium')
        plt.title(title, fontdict=font)
        plt.axis('equal')
        plt.tight_layout()
        plt.savefig(targetPath, bbox_inches='tight',
                    pad_inches=.5)  # exporting plotted PIE chart
        plt.close()  # closing this figure on which we just plotted a PIE chart
        return True
    except Exception:
        return False


if __name__ == '__main__':
    print('[!]This module is designed to be used as a backend handler')
    exit(0)
