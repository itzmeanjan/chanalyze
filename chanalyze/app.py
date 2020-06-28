#!/usr/bin/python3

from __future__ import annotations
from typing import List, Tuple, Dict
from functools import reduce
from sys import argv
from os.path import join, exists
from os import getenv
from matplotlib import pyplot as plt
from time import time
from multiprocessing import Process, Queue, cpu_count

from .util import (
    plotContributionInChatByUser,
    plotContributionOfUserByHour,
    shadeContactName,
    plotActivityOfUserByMinute,
    mergeMessagesFromUsersIntoSequence,
    classifyMessagesOfChatByDate,
    plotActivenessOfChatByDate,
    directoryBuilder,
    getConversationInitializers,
    plotConversationInitializerStat
)
from .model.chat import Chat
from .emoji_data.get import (
    exportToFile,
    importFromFile
)
from .emoji import (
    findNonASCIICharactersinText,
    findEmojisInText,
    findEmojiUsage,
    plotEmojiUsage
)


def _getSupportedOutputFormats() -> Dict[str, str]:
    '''
        Tries to determine supported backends in host machine,
        only these formats can be used for exporting a plot
    '''
    fig = plt.figure()

    formats = fig.canvas.get_supported_filetypes()

    plt.close(fig)
    return formats


def _makeOutputChoice() -> str:
    options = _getSupportedOutputFormats()
    if not options:
        return None

    for i, (k, v) in enumerate(options.items()):
        print('{} ) {} [ .{} ]'.format(i+1, v, k))

    try:
        choice = int(input('\n[?]Choose desired output format : '))
        if choice not in range(1, len(options) + 1):
            raise Exception('Bad Input')
        return list(options.keys())[choice-1]
    except EOFError:
        return None
    except Exception:
        return None


def _calculatePercentageOfSuccess(stat: List[bool]) -> float:
    '''
        Calculates rate of success in plotting ops
    '''
    return 0 if len(stat) == 0 else reduce(lambda acc, cur:
                                           acc+1 if cur else acc, stat, 0)/len(stat) * 100


def _parallelPlotting(chat: Chat, emojiData: List[int], sinkDirectory: str, extension: str) -> float:
    '''
        Implements process based paralleism,
        for each plotting task there's a new process,
        returning result of computation to parent by writing to Queue
    '''

    '''
        *list(
            map(
                lambda cur: Process(
                    target=plotContributionOfUserByHour,
                    args=(
                        cur.messages,
                        join(sinkDirectory,
                             'contributionInChatOf{}ByHour.{}'.format(
                                 '_'.join(cur.name.split(' ')), extension)),
                        '{}\'s Contribution in Chat [ {} - {} ]'
                        .format(cur.name,
                                chat.startDate.strftime('%d %b, %Y'),
                                chat.endDate.strftime('%d %b, %Y')),
                        q
                    )),
                chat.users
            )
        ),
        *list(
            map(
                lambda cur: Process(
                    target=plotActivityOfUserByMinute,
                    args=(
                        cur.messages,
                        join(sinkDirectory, 'detailedActivityOf{}InChatByMinute.{}'
                             .format(
                                 '_'.join(cur.name.split(' ')), extension)),
                        'Detailed Activity Of {} in Chat By Minute [ {} - {} ]'
                        .format(cur.name,
                                chat.startDate.strftime('%d %b, %Y'),
                                chat.endDate.strftime('%d %b, %Y')),
                        q
                    )),
                chat.users
            )
        ),
        Process(
            target=plotActivenessOfChatByDate,
            args=(
                classifyMessagesOfChatByDate(
                    mergeMessagesFromUsersIntoSequence(chat)),
                join(sinkDirectory, 'activenessOfChatByDate.{}'
                     .format(extension)),
                'Daily Activeness Of a Chat [ {} - {} ]'
                .format(chat.startDate.strftime('%d %b, %Y'),
                        chat.endDate.strftime('%d %b, %Y')),
                q
            )
        ),
        Process(
            target=plotConversationInitializerStat,
            args=(
                getConversationInitializers(chat),
                join(sinkDirectory,
                     'conversationInitializerStat.{}'.format(extension)),
                ('Conversation Initializers\' Statistics, using Mean Delay [ {} - {} ]'
                 .format(chat.startDate.strftime('%d %b, %Y'),
                         chat.endDate.strftime('%d %b, %Y')),
                 'Conversation Initializers\' Statistics, using Median Delay [ {} - {} ]'
                 .format(chat.startDate.strftime('%d %b, %Y'),
                         chat.endDate.strftime('%d %b, %Y'))),
                q
            )
        ),
        

    procs = [
        Process(
            target=plotContributionInChatByUser,
            args=(
                chat,
                join(sinkDirectory,
                     'participationInChatByUser.{}'
                     .format(extension)),
                'Participation of Users in Chat [ {} - {} ]'
                .format(chat.startDate.strftime('%d %b, %Y'),
                        chat.endDate.strftime('%d %b, %Y'))
            )
        ),
        Process(
            target=plotEmojiUsage,
            args=(
                findEmojiUsage(findEmojisInText(
                    findNonASCIICharactersinText(chat),
                    emojiData)),
                join(sinkDirectory,
                     'emojiUsage.{}'.format(extension)),
                'Top 7 Emoji(s) used in Chat [ {} - {} ]'
                .format(chat.startDate.strftime('%d %b, %Y'),
                        chat.endDate.strftime('%d %b, %Y'))
            )
        )
    ]
    '''
    results = []
    return _calculatePercentageOfSuccess(results)


def main():

    # extracts passed command line arguments
    def _getCMDArgs() -> Tuple[str, str]:
        return tuple(argv[1:len(argv)]) if len(argv) == 3 else (None, None)

    # prints usage of this script
    def _banner():
        print('\x1b[1;6;36;49m[+]chanalyze v0.3.4 - A simple WhatsApp Chat Analyzer\x1b[0m\n\n\t\x1b[3;30;47m$ chanalyze `path-to-exported-chat-file` `path-to-sink-directory`\x1b[0m\n\n[+]Author: Anjan Roy<anjanroy@yandex.com>\n[+]Source: https://github.com/itzmeanjan/chanalyze ( MIT Licensed )\n')

    startTime = time()
    endTime = startTime
    successRate = 0.0

    try:
        sourceFile, sinkDirectory = _getCMDArgs()
        # path to source file must be ending with `txt`, cause it's generally exported into a text file
        if not (sourceFile and sinkDirectory and sourceFile and sinkDirectory):
            _banner()
            raise Exception('Improper invokation !')

        directoryBuilder(sinkDirectory)
        if not (sourceFile.endswith('txt') and exists(sourceFile) and exists(sinkDirectory)):
            _banner()
            raise Exception('Invalid chat file !')

        _banner()
        # this instance will live throughout lifetime of this script
        chat = Chat.importFromText(sourceFile)
        emojiData = importFromFile() or exportToFile()

        if not emojiData:
            raise Exception('Unable to fetch emoji data')

        extension = _makeOutputChoice()
        if not extension:
            raise Exception('Invalid output format !')

        print('[*]Working ...')
        successRate = _parallelPlotting(
            chat, emojiData, sinkDirectory, extension)
        endTime = time()
    except KeyboardInterrupt:
        print('\n[!]Terminated')
        endTime = time()
    except Exception as e:
        print('[!]{}'.format(e))
        endTime = time()
    finally:
        print('[+]Success : {} % in {}s'
              .format(successRate,
                      endTime - startTime))
        return


if __name__ == '__main__':
    main()
