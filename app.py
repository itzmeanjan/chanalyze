#!/usr/bin/python3

from __future__ import annotations
from typing import List
from functools import reduce
try:
    from util import plotContributionInChatByUser, plotContributionOfUserByHour, shadeContactName, plotActivityOfUserByMinute, mergeMessagesFromUsersIntoSequence, classifyMessagesOfChatByDate, plotActivenessOfChatByDate
    from model.chat import Chat
except ImportError as e:
    print('[!]Module Unavailable: {}'.format(str(e)))
    exit(1)


def main() -> float:
    def __calculatePercentageOfSuccess__(stat: List[bool]) -> float:
        return reduce(lambda acc, cur:
                      acc+1 if cur else acc, stat, 0)/len(stat) * 100

    try:
        '''
                plotContributionInChatByUser(Chat.importFromText(
                    './data/private.txt'), './plots/participationInPrivateChatByUser.png', 'Visualization of Participation of Users in Chat'),
                plotContributionInChatByUser(Chat.importFromText(
                    './data/group.txt'), './plots/participationInGroupChatByUser.png', 'Visualization of Participation of Users in Chat'),
                *reduce(lambda acc, cur:
                        [plotContributionOfUserByHour(
                            cur.messages, './plots/contributionInPrivateChatOf{}ByHour.png'.format(
                                shadeContactName('_'.join(cur.name.split(' ')), percent=75)),
                            'Visualization of {}\'s Participation in Private Chat'.format(shadeContactName(cur.name, percent=75)))] + acc,
                        Chat.importFromText('./data/private.txt').users, []),
                *reduce(lambda acc, cur:
                        [plotContributionOfUserByHour(
                         cur.messages, './plots/contributionInGroupChatOf{}ByHour.png'.format(
                             shadeContactName('_'.join(cur.name.split(' ')), percent=75)),
                         'Visualization of {}\'s Participation in Group Chat'.format(shadeContactName(cur.name, percent=75)))] + acc,
                        Chat.importFromText('./data/group.txt').users, []),
                *reduce(lambda acc, cur:
                        [plotActivityOfUserByMinute(cur.messages,
                                                    './plots/detailedActivityOf{}InPrivateChatByMinute.svg'.format(
                                                        shadeContactName('_'.join(cur.name.split(' ')), percent=75)),
                                                    'Activity Of {} in Private Chat By Minute'.format(shadeContactName(cur.name, percent=75)))] + acc,
                        Chat.importFromText('./data/private.txt').users, []),
                *reduce(lambda acc, cur:
                        [plotActivityOfUserByMinute(cur.messages,
                                                    './plots/detailedActivityOf{}InGroupChatByMinute.svg'.format(
                                                        shadeContactName('_'.join(cur.name.split(' ')), percent=75)),
                                                    'Activity Of {} in Group Chat By Minute'.format(shadeContactName(cur.name, percent=75)))] + acc,
                        Chat.importFromText('./data/group.txt').users, [])
        '''
        return __calculatePercentageOfSuccess__(
            [
                plotActivenessOfChatByDate(
                    classifyMessagesOfChatByDate(mergeMessagesFromUsersIntoSequence(
                        Chat.importFromText('./data/private.txt'))), './plots/activenessOfPrivateChatByDate.svg', 'Daily Activeness Of a Private Chat'),
                plotActivenessOfChatByDate(
                    classifyMessagesOfChatByDate(mergeMessagesFromUsersIntoSequence(
                        Chat.importFromText('./data/group.txt'))), './plots/activenessOfGroupChatByDate.svg', 'Daily Activeness Of a Group Chat')
            ])
    except Exception:
        return 0.0


if __name__ == '__main__':
    try:
        print('[+] Success: {:.4f}%'.format(main()))
    except KeyboardInterrupt:
        print('\n[!]Terminated')
    finally:
        exit(0)
