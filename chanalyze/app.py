#!/usr/bin/python3

from __future__ import annotations
from typing import List, Tuple, Dict
from functools import reduce
from sys import argv
from os.path import join, exists
from os import getenv
from matplotlib import pyplot as plt
from time import time
from multiprocessing import cpu_count
import ray

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

# initializing ray - powering concurrent processing of plotting ops !!!
ray.init(num_cpus=cpu_count())


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
        Implements process based paralleism using `ray` module,
        all plotting work done concurrently !!!
    '''
    _ids = [
        plotContributionInChatByUser.remote(
            chat,
            join(sinkDirectory,
                 'participationInChatByUser.{}'
                 .format(extension)),
            'Participation of Users in Chat [ {} - {} ]'
            .format(chat.startDate.strftime('%d %b, %Y'),
                    chat.endDate.strftime('%d %b, %Y'))
        ),
        *list(
            map(
                lambda cur:
                plotContributionOfUserByHour.remote(
                    cur.messages,
                    join(sinkDirectory,
                         'contributionInChatOf{}ByHour.{}'.format(
                             '_'.join(cur.name.split(' ')), extension)),
                    '{}\'s Contribution in Chat [ {} - {} ]'
                    .format(cur.name,
                            chat.startDate.strftime('%d %b, %Y'),
                            chat.endDate.strftime('%d %b, %Y'))
                ),
                chat.users
            )
        ),
        *list(
            map(
                lambda cur:
                plotActivityOfUserByMinute.remote(
                    cur.messages,
                    join(sinkDirectory, 'detailedActivityOf{}InChatByMinute.{}'
                         .format(
                             '_'.join(cur.name.split(' ')), extension)),
                    'Detailed Activity Of {} in Chat By Minute [ {} - {} ]'
                    .format(cur.name,
                            chat.startDate.strftime('%d %b, %Y'),
                            chat.endDate.strftime('%d %b, %Y'))
                ),
                chat.users
            )
        ),
        plotActivenessOfChatByDate.remote(
            classifyMessagesOfChatByDate(
                mergeMessagesFromUsersIntoSequence(chat)),
            join(sinkDirectory, 'activenessOfChatByDate.{}'
                 .format(extension)),
            'Daily Activeness Of a Chat [ {} - {} ]'
            .format(chat.startDate.strftime('%d %b, %Y'),
                    chat.endDate.strftime('%d %b, %Y'))
        ),
        plotConversationInitializerStat.remote(
            getConversationInitializers(chat),
            join(sinkDirectory,
                 'conversationInitializerStat.{}'.format(extension)),
            ('Conversation Initializers\' Statistics, using Mean Delay [ {} - {} ]'
             .format(chat.startDate.strftime('%d %b, %Y'),
                     chat.endDate.strftime('%d %b, %Y')),
             'Conversation Initializers\' Statistics, using Median Delay [ {} - {} ]'
             .format(chat.startDate.strftime('%d %b, %Y'),
                     chat.endDate.strftime('%d %b, %Y')))
        ),
        plotEmojiUsage.remote(
            findEmojiUsage(findEmojisInText(
                findNonASCIICharactersinText(chat),
                emojiData)),
            join(sinkDirectory,
                 'emojiUsage.{}'.format(extension)),
            'Top 7 Emoji(s) used in Chat [ {} - {} ]'
            .format(chat.startDate.strftime('%d %b, %Y'),
                    chat.endDate.strftime('%d %b, %Y'))
        )
    ]

    # awaiting result of all plotting functions invoked
    return _calculatePercentageOfSuccess(ray.get(_ids))


def main():

    # extracts passed command line arguments
    def _getCMDArgs() -> Tuple[str, str]:
        return tuple(argv[1:len(argv)]) if len(argv) == 3 else (None, None)

    # prints usage of this script
    def _banner():
        print('\x1b[1;6;36;49m[+]chanalyze v0.3.5 - A simple WhatsApp Chat Analyzer\x1b[0m\n\n\t\x1b[3;30;47m$ chanalyze `path-to-exported-chat-file` `path-to-sink-directory`\x1b[0m\n\n[+]Author: Anjan Roy<anjanroy@yandex.com>\n[+]Source: https://github.com/itzmeanjan/chanalyze ( MIT Licensed )\n')

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
        ray.shutdown()
        return


if __name__ == '__main__':
    main()
