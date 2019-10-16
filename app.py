#!/usr/bin/python3

from __future__ import annotations
from typing import List, Tuple
from functools import reduce
from sys import argv
from os.path import join, exists
try:
    from util import plotContributionInChatByUser, plotContributionOfUserByHour, shadeContactName, plotActivityOfUserByMinute, mergeMessagesFromUsersIntoSequence, classifyMessagesOfChatByDate, plotActivenessOfChatByDate, directoryBuilder, getConversationInitializers, plotConversationInitializerStat
    from model.chat import Chat
except ImportError as e:
    print('[!]Module Unavailable: {}'.format(str(e)))
    exit(1)


def main() -> float:
    def __calculatePercentageOfSuccess__(stat: List[bool]) -> float:
        return reduce(lambda acc, cur:
                      acc+1 if cur else acc, stat, 0)/len(stat) * 100

    # extracts passed command line arguments
    def __getCMDArgs__() -> Tuple[str, str]:
        return tuple(argv[1:len(argv)]) if len(argv) == 3 else (None, None)

    # prints usage of this script
    def __usage__():
        print('\x1b[1;6;36;49m[+]chanalyze v0.1.1 - A simple WhatsApp Chat Analyzer\x1b[0m\n\n\t\x1b[3;30;47m$ chanalyze `path-to-exported-chat-file` `path-to-sink-directory`\x1b[0m\n\n[+]Author: Anjan Roy<anjanroy@yandex.com>\n[+]Source: https://github.com/itzmeanjan/chanalyze ( MIT Licensed )\n')

    try:
        sourceFile, sinkDirectory = __getCMDArgs__()
        # path to source file must be ending with `txt`, cause it's generally exported into a text file
        if not sourceFile or not sinkDirectory or not sourceFile.endswith('txt') or not exists(sourceFile):
            __usage__()
            raise Exception('Improper invokation !!!')
        directoryBuilder(sinkDirectory)
        # this instance will live throughout lifetime of this script
        chat = Chat.importFromText(sourceFile)
        print(
            '\x1b[1;6;36;49m[+]chanalyze v0.1.1 - A simple WhatsApp Chat Analyzer\x1b[0m\n[*]Working ...')
        return __calculatePercentageOfSuccess__(
            [
                plotContributionInChatByUser(
                    chat,
                    join(sinkDirectory, 'participationInChatByUser.jpg'),
                    'Participation of Users in Chat ( in terms of Percentage )'),
                *reduce(lambda acc, cur:
                        [plotContributionOfUserByHour(
                            cur.messages,
                            join(sinkDirectory, 'contributionInChatOf{}ByHour.jpg'.format(
                                '_'.join(cur.name.split(' ')))),
                            '{}\'s Contribution in Chat'.format(cur.name))] + acc,
                        chat.users, []),
                *reduce(lambda acc, cur:
                        [plotActivityOfUserByMinute(
                            cur.messages,
                            join(sinkDirectory, 'detailedActivityOf{}InChatByMinute.jpg'.format(
                                '_'.join(cur.name.split(' ')))),
                            'Detailed Activity Of {} in Chat By Minute'.format(cur.name))] + acc,
                        chat.users, []),
                plotActivenessOfChatByDate(
                    classifyMessagesOfChatByDate(
                        mergeMessagesFromUsersIntoSequence(chat)),
                    join(sinkDirectory, 'activenessOfChatByDate.jpg'),
                    'Daily Activeness Of a Chat'),
                plotConversationInitializerStat(
                    getConversationInitializers(chat),
                    join(sinkDirectory, 'conversationInitializerStat.jpg'),
                    ('Conversation Initializers\' Statistics ( using Mean Delay )',
                     'Conversation Initializers\' Statistics ( using Median Delay )'))
            ])
    except Exception:
        return 0.0


if __name__ == '__main__':
    try:
        print('[#]Success: {:.4f}%'.format(main()))
    except KeyboardInterrupt:
        print('\n[!]Terminated')
    finally:
        exit(0)
