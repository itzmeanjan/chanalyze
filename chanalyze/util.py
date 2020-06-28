#!/usr/bin/python3

from __future__ import annotations
from os.path import abspath, dirname, exists
from os import mkdir
from functools import reduce
from typing import Dict, List, Tuple
from collections import OrderedDict, Counter
from math import ceil, sqrt
from datetime import datetime, date, time
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator, PercentFormatter, StrMethodFormatter, NullLocator, NullFormatter
from matplotlib.dates import HourLocator, DateFormatter, MinuteLocator, MonthLocator, DayLocator
import ray

from .model.chat import Chat
from .model.message import Message, MessageIndex
from .model.timePeriod import TimePeriod
from .model.msgInMinute import MessagesSentInMinute, MessagesSentInADay
from .model.msgOnDate import MessagesSentOnDate
from .model.msgDiff import DifferenceBetweenMessages


def directoryBuilder(targetPath: str):
    '''
        Checks whether this directory already exists or not.
        if not, creates it
    '''
    dirName = abspath(targetPath)
    if not exists(dirName):
        mkdir(dirName)


def shadeContactName(name: str, percent: float = 50.0, where: str = 'f') -> str:
    '''
        Shades first half of characters of Contact by `*`, for sake of privacy
    '''
    return '*'*ceil(len(name)*percent/100)\
        + name[ceil(len(name)*percent/100):] if where.lower() == 'f' else name[:-ceil(len(name)*percent/100)]\
        + '*'*ceil(len(name)*percent/100)


@ray.remote
def plotContributionInChatByUser(chat: Chat, targetPath: str, title: str, top: int = 25) -> bool:
    '''
        How much a certain person contributed to a Chat 
        plotted into a Bar Chart ( shows contribution in terms of percentage )
    '''
    try:
        # considering only top 25 contributors in Chat
        y = reduce(lambda acc, cur: acc + [cur] if len(acc) < (top+1) else acc,
                   sorted([i.name for i in chat.users],
                          key=lambda e: len(chat.getUser(e).messages),
                          reverse=True),
                   [])
        # y = sorted([i.name for i in chat.users],
        #           key=lambda e: len(chat.getUser(e).messages), reverse=True)
        y_pos = range(len(y))
        x = [(len(chat.getUser(i).messages) / chat.messageCount) * 100 for i in y]
        # y = [shadeContactName(i, percent=75) for i in y]
        with plt.style.context('Solarize_Light2'):
            font = {
                'family': 'serif',
                'color': '#000000',
                'weight': 'normal',
                'size': 10
            }
            fig = plt.figure(figsize=(24, 12), dpi=100)
            plt.xlim((0, 100))
            fig.gca().xaxis.set_major_locator(MultipleLocator(10))
            fig.gca().xaxis.set_major_formatter(PercentFormatter())
            fig.gca().xaxis.set_minor_locator(MultipleLocator(1))
            fig.gca().yaxis.set_ticks(y_pos)
            fig.gca().yaxis.set_ticklabels(y)
            plt.barh(y_pos, x, align='center',
                     color='deepskyblue', lw=1.6)
            plt.xlabel('Percentage of Participation in Chat',
                       fontdict=font, labelpad=12)
            plt.title(title,
                      fontdict=font, pad=12)
            fig.tight_layout()
            fig.savefig(targetPath, bbox_inches='tight', pad_inches=.5)
            plt.close(fig=fig)
        return True
    except Exception:
        return False


@ray.remote
def plotContributionOfUserByHour(messages: List[Message], targetPath: str, title: str) -> bool:

    def __buildStatusHolder__(holder: Dict[str, int], current: Message) -> Dict[str, int]:
        tm = current.timeStamp.timetz()
        seconds = tm.hour*3600 + tm.minute*60
        found = str(
            reduce(lambda acc, cur: cur if seconds in cur else acc, ranges, None))
        holder.update({found: holder.get(found, 0)+1})
        return holder

    try:
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


@ray.remote
def plotActivityOfUserByMinute(messages: List[Message], targetPath: str, title: str) -> bool:
    '''
        Plots a chart, showing at which minute of
        day ( there's 1440 minutes in a day )
        this participant is how much active ( in this chat ),
        over period of time, for which we've track record ( in exported chat )
    '''

    def _determineMajorLocatorSpacing(maxV: int) -> int:
        '''
            Determines how to place major & minor locators on both axes,
            so that we don't over-populate axes

            Max allowed number of major locators 20
        '''
        maxV = maxV if maxV % 10 == 0 else (maxV - maxV % 10 + 10)
        return round(sqrt(maxV))

    def __buildEachMinuteStatHolder__(holder: MessagesSentInADay, current: Message) -> MessagesSentInADay:
        '''
            This is to be called for each element
            present in `messages`, so that
            we can keep track of #-of messages
            sent in each minute
        '''
        holder.findARecord(current.timeStamp.timetz()).incrementCount()
        return holder

    def __splitIntoParts__(whole, partCount: int):
        '''
            Splits a collection of objects into
            equal parts of requested count i.e.
            returns a collection of ( sub ) collections
        '''
        if not whole:
            return [None] * partCount

        lengthOfEachPart = len(whole)//partCount
        return [whole[i*lengthOfEachPart:(i+1)*lengthOfEachPart]
                for i in range(partCount)]

    try:
        statByMinute = reduce(__buildEachMinuteStatHolder__, messages, MessagesSentInADay([
            MessagesSentInMinute(i, j, 0) for i in range(0, 24) for j in range(0, 60)]))
        tmpX = [datetime.combine(date(2000, 1, 1), time(i.hour, i.minute))
                for i in statByMinute.records]
        x1, x2, x3, x4 = __splitIntoParts__(tmpX, 4)
        if not (x1 and x2 and x3 and x4):
            return False

        y1, y2, y3, y4 = __splitIntoParts__(
            [statByMinute.findARecord(i.timetz()).count for i in tmpX], 4)
        if not (y1 and y2 and y3 and y4):
            return False

        # this will help us in setting max value on Y-axis
        # and no doubt min value is 0
        maxMsgCount = max([max([max([max(y1)] + y2)] + y3)] + y4) + 1
        locatorSpacingAlongY = _determineMajorLocatorSpacing(maxMsgCount)
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
            axes1.yaxis.set_major_locator(
                MultipleLocator(locatorSpacingAlongY))
            axes1.yaxis.set_major_formatter(StrMethodFormatter('{x}'))
            axes1.yaxis.set_minor_locator(NullLocator())
            axes2.yaxis.set_major_locator(
                MultipleLocator(locatorSpacingAlongY))
            axes2.yaxis.set_major_formatter(StrMethodFormatter('{x}'))
            axes2.yaxis.set_minor_locator(NullLocator())
            axes3.yaxis.set_major_locator(
                MultipleLocator(locatorSpacingAlongY))
            axes3.yaxis.set_major_formatter(StrMethodFormatter('{x}'))
            axes3.yaxis.set_minor_locator(NullLocator())
            axes4.yaxis.set_major_locator(
                MultipleLocator(locatorSpacingAlongY))
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


def mergeMessagesFromUsersIntoSequence(chat: Chat) -> List[Message]:
    '''
        Takes a Chat object & returns a sequenced list of messages,
        as they appeared in original chat
    '''
    currentMsgIdx = 0
    nextMessageToBeVisitedForEachParticipant = [0]*len(chat.users)
    sequence = []
    for _ in range(chat.messageCount):
        for j, k in enumerate(chat.users):
            try:
                # there may be a case when we're trying to reach to some message index for a certain user `k`, which doesn't even exist
                # then we may require to handle one exception
                msg = k.messages[nextMessageToBeVisitedForEachParticipant[j]]
                if msg.index == currentMsgIdx:
                    sequence.append(msg)
                    currentMsgIdx += 1
                    nextMessageToBeVisitedForEachParticipant[j] += 1
                    break
            except Exception:
                continue
    return sequence


def classifyMessagesOfChatByDate(messages: List[Message]) -> List[MessagesSentOnDate]:
    '''
        Classifies a collection of messages
        by Date on which they were sent.

        So no doubt this may produce really large dataset in case
        of lengthy chats

        Returns a collection of MessagesSentOnDate objects,
        each of them holding # of messages trasmitted
        among chat participants on that certain date
    '''
    def __updateStat__(acc: List[MessagesSentOnDate], cur: Message) -> List[MessagesSentOnDate]:
        found = reduce(lambda accInner, curInner: curInner if curInner.currentDate ==
                       cur.timeStamp.date() else accInner, acc, None)
        if not found:
            acc.append(MessagesSentOnDate(cur.timeStamp.date(), 1))
        else:
            found.incrementBy()
        return acc
    return reduce(__updateStat__, messages, [])


@ray.remote
def plotActivenessOfChatByDate(messages: List[MessagesSentOnDate], targetPath: str, title: str) -> bool:
    '''
        Tries to depict how all participating users of a Chat
        contributed to traffic of that Chat by Day

        If we've a very long chat ( spreading across years ),
        then we'll simply accumulate it into a year ( 
        holding whole record into 365/366 days )

        It can be useful in understanding at which day of Year,
        people of this chat preferred to talk mostly
    '''
    def _determineMajorLocatorSpacing(data: List[int]) -> int:
        '''
            Determines how to place major & minor locators on both axes,
            so that we don't over-populate axes

            Max allowed number of major locators 20
        '''
        maxV = max(data)
        # finds out next round number
        maxV = maxV if maxV % 10 == 0 else (maxV - maxV % 10 + 10)
        return round(sqrt(maxV))

    def __accumulateData__(data: List[MessagesSentOnDate]) -> List[MessagesSentOnDate]:
        def __updateCount__(acc: List[MessagesSentOnDate], cur: MessagesSentOnDate) -> List[MessagesSentOnDate]:
            found = reduce(lambda accInner, curInner: curInner if cur.currentDate.day ==
                           curInner.currentDate.day and cur.currentDate.month == curInner.currentDate.month
                           else accInner, acc, None)
            if not found:
                acc.append(MessagesSentOnDate(date(
                    1996, cur.currentDate.month, cur.currentDate.day), cur.count))  # using a year, which was leap year, cause it won't throw one error when trying to define a date having 29th day in Feb
            else:
                found.incrementBy(cur.count)
            return acc
        return reduce(__updateCount__, data, [])
    try:
        messages = __accumulateData__(messages)
        x = [i.currentDate for i in messages]
        y = [i.count for i in messages]
        majorLocatorCount = _determineMajorLocatorSpacing(y)
        with plt.style.context('Solarize_Light2'):
            font = {
                'family': 'serif',
                'color': '#000000',
                'weight': 'normal',
                'size': 16
            }
            plt.figure(figsize=(24, 12), dpi=100)
            plt.gca().xaxis.set_major_locator(MonthLocator())
            plt.gca().xaxis.set_major_formatter(DateFormatter('%b'))
            plt.gca().xaxis.set_minor_locator(DayLocator())
            plt.gca().xaxis.set_minor_formatter(DateFormatter('%d'))
            plt.gca().yaxis.set_major_locator(MultipleLocator(majorLocatorCount))
            plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x}'))
            plt.gca().yaxis.set_minor_locator(MultipleLocator(majorLocatorCount / 2))
            plt.ylim(-5, max(y)+5)
            plt.plot(x, y, 'ro-', lw=.8)
            plt.xlabel('Time', fontdict=font, labelpad=14)
            plt.ylabel('#-of messages transferred', fontdict=font, labelpad=14)
            plt.title(title, fontdict=font, pad=14)
            plt.tight_layout()
            plt.savefig(targetPath, bbox_inches='tight',
                        pad_inches=.4, quality=95, dpi=100)  # exporting plotting into a file ( image )
            plt.close()
        return True
    except Exception:
        return False


def getConversationInitializers(chat: Chat) -> Tuple[Counter, Counter]:
    '''
        Get how many times which chat participant started
        a conversation ( applicable for both Private & Group chat )

        By a conversation in a Chat, I mean, when a collection of messages
        are/ were transmitted between these participants, after a certain delay
        & may be lasted for a while

        For finding that I calculated elapsed time between all messages
        of this Chat. Now I find unique delay values. From that meanDelay
        & medianDelay

        Now I filter out all those message senders
        who sent some message ( using message index )
        having delay value greater than or equal to meanDelay
        & medianDelay, and find frequency of them
    '''
    messages = mergeMessagesFromUsersIntoSequence(chat)
    diff = [DifferenceBetweenMessages(i, i+1, int((messages[i+1].timeStamp - j.timeStamp).total_seconds()))
            for i, j in enumerate(messages[:-1])]
    unique = sorted(reduce(lambda acc, cur: [
        cur] + acc if cur not in acc else acc, diff, []),
        key=lambda e: e.elapsedTime)
    if not unique:
        return (None, None)

    meanDelay = sum([i.elapsedTime for i in unique])//len(unique)
    medianDelay = unique[len(unique)//2].elapsedTime
    return (Counter(map(lambda e: chat.getUserByMessageId(e.msgTwo).name,
                        filter(lambda e: e.elapsedTime >= meanDelay, diff))),
            Counter(map(lambda e: chat.getUserByMessageId(e.msgTwo).name,
                        filter(lambda e: e.elapsedTime >= medianDelay, diff))))


@ray.remote
def plotConversationInitializerStat(data: Tuple[Counter, Counter], targetPath: str, title: Tuple[str, str]) -> bool:
    try:
        if not (data[0] and data[1]):
            return False

        y1, y2 = [i for i in data[0]], [i for i in data[1]]
        x1, x2 = [data[0][i] for i in y1], [data[1][i] for i in y2]
        # contact name/ number shading is temporarily disabled
        # y1, y2 = [shadeContactName(i, percent=75) for i in y1], [shadeContactName(i, percent=75) for i in y2]
        total1, total2 = sum(x1), sum(x2)
        if not (total1 and total2):
            return False

        x1, x2 = [i*100/total1 for i in x1], [i*100/total2 for i in x2]
        with plt.style.context('Solarize_Light2'):
            font = {
                'family': 'serif',
                'color': '#000000',
                'weight': 'normal',
                'size': 12
            }
            _, (axes1, axes2) = plt.subplots(1, 2, figsize=(24, 12), dpi=12)
            # handling X-axis ticks & labels for subplot 1 ( on left )
            axes1.set_xlim(0, 100)
            axes1.xaxis.set_major_locator(MultipleLocator(10))
            axes1.xaxis.set_major_formatter(PercentFormatter())
            axes1.xaxis.set_minor_locator(MultipleLocator(1))
            axes1.xaxis.set_minor_formatter(NullFormatter())
            # handling X-axis ticks & labels for subplot 2 ( on right )
            axes2.set_xlim(0, 100)
            axes2.xaxis.set_major_locator(MultipleLocator(10))
            axes2.xaxis.set_major_formatter(PercentFormatter())
            axes2.xaxis.set_minor_locator(MultipleLocator(1))
            axes2.xaxis.set_minor_formatter(NullFormatter())
            axes1.barh(y1, x1, align='center', color='deepskyblue', lw=1.5)
            axes2.barh(y2, x2, align='center', color='deepskyblue', lw=1.5)
            axes1.set_xlabel('Percentage of Conversations Started',
                             fontdict=font, labelpad=16)
            axes2.set_xlabel('Percentage of Conversations Started',
                             fontdict=font, labelpad=16)
            axes1.set_title(title[0], fontdict=font, pad=16)
            axes2.set_title(title[1], fontdict=font, pad=16)
            plt.tight_layout()
            plt.savefig(targetPath, bbox_inches='tight',
                        pad_inches=.4, quality=95, dpi=100)
            plt.close()  # don't miss this, it's required. Otherwise it might result into memory leaking
            # And no doubt too much memory will stay occupied
        return True
    except Exception:
        return False


if __name__ == '__main__':
    print('[!]This module is designed to be used as a backend handler')
    exit(0)
