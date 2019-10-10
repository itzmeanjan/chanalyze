#!/usr/bin/python3

from __future__ import annotations
from os.path import abspath, dirname, exists
from os import mkdir
from functools import reduce
from typing import Dict, List
from collections import OrderedDict
from math import ceil
from datetime import datetime, date, time
try:
    from matplotlib import pyplot as plt
    from matplotlib.ticker import MultipleLocator, PercentFormatter, StrMethodFormatter, NullLocator
    from matplotlib.dates import HourLocator, DateFormatter, MinuteLocator
    from model.chat import Chat
    from model.user import User
    from model.message import Message
    from model.timePeriod import TimePeriod
    from model.msgInMinute import MessagesSentInMinute, MessagesSentInADay
    from model.msgOnDate import MessagesSentOnDate
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

'''
    Plots a chart, showing at which minute of
    day ( there's 1440 minutes in a day )
    this participant is how much active ( in this chat ),
    over period of time, for which we've track record ( in exported chat )
'''
def plotActivityOfUserByMinute(messages: List[Message], targetPath: str, title: str) -> bool:
    '''
        This is to be called for each element
        present in `messages`, so that
        we can keep track of #-of messages
        sent in each minute
    '''
    def __buildEachMinuteStatHolder__(holder: MessagesSentInADay, current: Message) -> MessagesSentInADay:
        holder.findARecord(current.timeStamp.timetz()).incrementCount()
        return holder
    '''
        Splits a collection of objects into
        equal parts of requested count i.e.
        returns a collection of ( sub ) collections
    '''
    def __splitIntoParts__(whole, partCount: int):
        lengthOfEachPart = len(whole)//partCount
        return [whole[i*lengthOfEachPart:(i+1)*lengthOfEachPart]
                for i in range(partCount)]

    try:
        directoryBuilder(targetPath)
        statByMinute = reduce(__buildEachMinuteStatHolder__, messages, MessagesSentInADay([
            MessagesSentInMinute(i, j, 0) for i in range(0, 24) for j in range(0, 60)]))
        tmpX = [datetime.combine(date(2000, 1, 1), time(i.hour, i.minute))
                for i in statByMinute.records]
        x1, x2, x3, x4 = __splitIntoParts__(tmpX, 4)
        y1, y2, y3, y4 = __splitIntoParts__(
            [statByMinute.findARecord(i.timetz()).count for i in tmpX], 4)
        # this will help us in setting max value on Y-axis
        # and no doubt min value is 0
        maxMsgCount = max([max([max([max(y1)] + y2)] + y3)] + y4) + 1
        with plt.style.context('ggplot'):
            font = {
                'family': 'serif',
                'color': '#000000',
                'weight': 'normal',
                'size': 10
            }
            _, ((axes1, axes2), (axes3, axes4)) = plt.subplots(
                2, 2, figsize=(24, 12), dpi=100)  # creating 4 subplots in a Figure
            axes1.xaxis.set_major_locator(HourLocator())
            axes1.xaxis.set_major_formatter(DateFormatter('%I:%M %p'))
            axes1.xaxis.set_minor_locator(MinuteLocator())
            axes2.xaxis.set_major_locator(HourLocator())
            axes2.xaxis.set_major_formatter(DateFormatter('%I:%M %p'))
            axes2.xaxis.set_minor_locator(MinuteLocator())
            axes3.xaxis.set_major_locator(HourLocator())
            axes3.xaxis.set_major_formatter(DateFormatter('%I:%M %p'))
            axes3.xaxis.set_minor_locator(MinuteLocator())
            axes4.xaxis.set_major_locator(HourLocator())
            axes4.xaxis.set_major_formatter(DateFormatter('%I:%M %p'))
            axes4.xaxis.set_minor_locator(MinuteLocator())
            # setting formatting for Y-axis ( for all subplots )
            axes1.yaxis.set_major_locator(MultipleLocator(1))
            axes1.yaxis.set_major_formatter(StrMethodFormatter('{x}'))
            axes1.yaxis.set_minor_locator(NullLocator())
            axes2.yaxis.set_major_locator(MultipleLocator(1))
            axes2.yaxis.set_major_formatter(StrMethodFormatter('{x}'))
            axes2.yaxis.set_minor_locator(NullLocator())
            axes3.yaxis.set_major_locator(MultipleLocator(1))
            axes3.yaxis.set_major_formatter(StrMethodFormatter('{x}'))
            axes3.yaxis.set_minor_locator(NullLocator())
            axes4.yaxis.set_major_locator(MultipleLocator(1))
            axes4.yaxis.set_major_formatter(StrMethodFormatter('{x}'))
            axes4.yaxis.set_minor_locator(NullLocator())
            # setting limit of tickers along X axis ( time axis )
            # axes1.set_xlim(x1[0], x1[-1])
            # axes2.set_xlim(x2[0], x2[-1])
            # axes3.set_xlim(x3[0], x3[-1])
            # axes4.set_xlim(x4[0], x4[-1])
            # setting limit of ticker values along Y axis ( #-of messages sent in that minute )
            axes1.set_ylim(0, maxMsgCount)
            axes2.set_ylim(0, maxMsgCount)
            axes3.set_ylim(0, maxMsgCount)
            axes4.set_ylim(0, maxMsgCount)
            # plotting data
            axes1.plot(x1, y1, 'r-', lw=.5)
            axes2.plot(x2, y2, 'r-', lw=.5)
            axes3.plot(x3, y3, 'r-', lw=.5)
            axes4.plot(x4, y4, 'r-', lw=.5)
            axes1.set_xlabel('Time',
                             fontdict=font, labelpad=12)
            axes1.set_ylabel('#-of Messages Sent',
                             fontdict=font, labelpad=12)
            axes2.set_xlabel('Time',
                             fontdict=font, labelpad=12)
            axes2.set_ylabel('#-of Messages Sent',
                             fontdict=font, labelpad=12)
            axes3.set_xlabel('Time',
                             fontdict=font, labelpad=12)
            axes3.set_ylabel('#-of Messages Sent',
                             fontdict=font, labelpad=12)
            axes4.set_xlabel('Time',
                             fontdict=font, labelpad=12)
            axes4.set_ylabel('#-of Messages Sent',
                             fontdict=font, labelpad=12)
            axes1.set_title(title,
                            fontdict=font, pad=12)
            axes2.set_title(title,
                            fontdict=font, pad=12)
            axes3.set_title(title,
                            fontdict=font, pad=12)
            axes4.set_title(title,
                            fontdict=font, pad=12)
            plt.tight_layout()
            plt.savefig(targetPath, bbox_inches='tight',
                        pad_inches=.2, quality=95, dpi=100)  # exporting plotting into a file ( image )
            plt.close()  # this is required, closing drawing canvas
        return True
    except Exception:
        return False


'''
    Takes a Chat object & returns a sequenced list of messages,
    as they appeared in original chat
'''


def mergeMessagesFromUsersIntoSequence(chat: Chat) -> List[Message]:
    currentMsgIdx = 0
    nextMessageToBeVisitedForEachParticipant = [0]*len(chat.users)
    sequence = []
    for _ in range(chat.messageCount):
        for j, k in enumerate(chat.users):
            msg = k.messages[nextMessageToBeVisitedForEachParticipant[j]]
            if msg.index == currentMsgIdx:
                sequence.append(msg)
                currentMsgIdx += 1
                nextMessageToBeVisitedForEachParticipant[j] += 1
                break
    return sequence


'''
    Classifies a collection of messages
    by Date on which they were sent.

    So no doubt this may produce really large dataset in case
    of lengthy chats

    Returns a collection of MessagesSentOnDate objects, 
    each of them holding # of messages trasmitted
    among chat participants on that certain date
'''


def classifyMessagesOfChatByDate(messages: List[Message]) -> List[MessagesSentOnDate]:
    def __updateStat__(acc: List[MessagesSentOnDate], cur: Message) -> List[MessagesSentOnDate]:
        found = reduce(lambda accInner, curInner: curInner if curInner.currentDate ==
                       cur.timeStamp.date() else accInner, acc, None)
        if not found:
            acc.append(MessagesSentOnDate(cur.timeStamp.date(), 1))
        else:
            found.incrementBy()
        return acc
    return reduce(__updateStat__, messages, [])


if __name__ == '__main__':
    print('[!]This module is designed to be used as a backend handler')
    exit(0)
