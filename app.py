#!/usr/bin/python3

from __future__ import annotations
from typing import List
from functools import reduce
try:
    from util import plotContributionInChatByUser, plotContributionOfUserByHour, shadeContactName
    from model.chat import Chat
except ImportError as e:
    print('[!]Module Unavailable: {}'.format(str(e)))
    exit(1)


def main() -> float:
    def __calculatePercentageOfSuccess__(stat: List[bool]) -> float:
        return reduce(lambda acc, cur:
                      acc+1 if cur else acc, stat, 0)/len(stat) * 100

    try:
        return __calculatePercentageOfSuccess__(
            [  # plotContributionInChatByUser(Chat.importFromText('./data/private.txt'), './plots/participationInPrivateChatByUser.png', 'Visualization of Participation of Users in Chat'),
                # plotContributionInChatByUser(Chat.importFromText(
                #  './data/group.txt'), './plots/participationInGroupChatByUser.png', 'Visualization of Participation of Users in Chat'),
                *reduce(lambda acc, cur:
                        [plotContributionOfUserByHour(
                            cur.messages, './plots/contributionInPrivateChatOf{}ByHour.png'.format(
                                shadeContactName('_'.join(cur.name.split(' ')))),
                            'Visualization of {}\'s Participation in Private Chat'.format(shadeContactName(cur.name)))] + acc,
                        Chat.importFromText('./data/private.txt').users, [])])
    except Exception:
        return 0.0


if __name__ == '__main__':
    try:
        print('[+] Success: {:.4f}%'.format(main()))
    except KeyboardInterrupt:
        print('\n[!]Terminated')
    finally:
        exit(0)
