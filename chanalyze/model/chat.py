#!/usr/bin/python3

from __future__ import annotations
from typing import List, Tuple
from re import compile as reg_compile, Pattern
from functools import reduce
from datetime import datetime

from .message import Message, MessageIndex
from .user import User


class Chat(object):
    '''
        A whole chat, which is generally exported into a text file ( *.txt )
        from WhatsApp, is read and processed & converted into Chat object.

        *Now holding easily retrievable information related to chat time span,
        can be useful in setting an informative title in plots*
    '''

    def __init__(self, users: List[User]):
        self.users = users
        self._messageCount = 0
        # this two can be used in plot titles to denote
        # chat expansion period in better way
        self._startDate = None
        self._endDate = None

    @property
    def messageCount(self) -> int:
        '''
            Returns calculated # of messages present in this chat
        '''
        return self._messageCount

    @messageCount.setter
    def messageCount(self, v):
        self._messageCount = v

    @property
    def startDate(self) -> datetime:
        try:
            return datetime.strptime(self._startDate, r'%d/%m/%y, %I:%M %p')
        except ValueError:
            return datetime.strptime(self._startDate, r'%d/%m/%Y, %I:%M %p')
        except Exception:
            return self._startDate

    @startDate.setter
    def startDate(self, dt):
        self._startDate = dt

    @property
    def endDate(self) -> datetime:
        try:
            return datetime.strptime(self._endDate, r'%d/%m/%y, %I:%M %p')
        except ValueError:
            return datetime.strptime(self._endDate, r'%d/%m/%Y, %I:%M %p')
        except Exception:
            return self._endDate

    @endDate.setter
    def endDate(self, dt):
        self._endDate = dt

    def getUser(self, name: str) -> User:
        '''
            Finds out whether a certain User participated in this chat or not
            ( by its name )

            In case of failure, returns None
        '''
        return reduce(lambda acc, cur: cur if cur.name ==
                      name else acc, self.users, None)

    def getUserByMessageId(self, idx: int) -> User:
        '''
            Helps in finding which user sent a certain message,
            by its index

            In case of invalid message index, returns None
        '''
        return None if idx < 0 or idx >= self.messageCount else reduce(lambda acc, cur:
                                                                       cur if reduce(
                                                                           lambda accInner, curInner: True if curInner.index == idx else accInner,
                                                                           cur.messages, False) else acc,
                                                                       self.users, None)

    @staticmethod
    def importFromText(filePath: str) -> Chat:
        '''
            Given text file path, returns chat object, 
            containing whole chat, which can be 
            easily played around with 
        '''

        def __getRegex__() -> Pattern:
            '''
                Regex to be used for extracting timestamp of
                a certain message from `*.txt` file
            '''
            return reg_compile(
                r'(\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}\:\d{1,2} [a|p]m)')

        def __splitByDate__(pattern: Pattern, content: str) -> List[str]:
            '''
                splitting whole *.txt file content using
                date extraction regex we just built
            '''
            return pattern.split(content)[1:]

        def __groupify__(splitted: List[str]) -> List[Tuple[str, str]]:
            '''
                In previous closure we splitted whole text file content by date,
                which needs to be fixed by pairing messages with its corresponding timestamp
            '''
            grouped = []
            for i in range(0, len(splitted), 2):
                grouped.append((splitted[i], splitted[i+1]))

            # setting start and end time of chat under lens
            obj.startDate = grouped[0][0]
            obj.endDate = grouped[-1][0]

            return grouped

        def __getUser__(text: str) -> str:
            '''
                Helps in extracting participating user name from message ( text )
            '''
            matchObj = reg_compile(r'(?<=\s-\s).+?(?=:)').search(text)
            return matchObj.group() if matchObj else ''

        def __getMessage__(text: str) -> str:
            '''
                Extracts actual message sent by a certain user using regex
            '''
            return reg_compile(r'\s-\s.+?(?=:):\s*').sub('', text)

        def __createUserObject__(acc: List[User], content: Tuple[str, str]) -> List[User]:
            '''
                Construction of User objects ( who participated in chat ) along with
                messages sent by them, done in this closure
            '''
            # if we can't extract username from message text, it's not a message of this chat, so we just ignore it
            userName = __getUser__(content[1])
            if not userName:
                return acc  # returning in unchanged form
            msg = Message(msgIndex.index, __getMessage__(
                content[1]), content[0])

            # updating count of message in chat
            obj.messageCount = obj.messageCount + 1

            # incrementing index for next message, which lets us sequentially ordering messages as they appeared in chat
            msgIndex.increment()
            found = reduce(lambda accInner, curInner: curInner if curInner.name ==
                           userName else accInner, acc, None)
            if not found:
                acc.append(User(userName, [msg]))
            else:
                found.messages.append(msg)
            return acc

        obj = Chat([])
        msgIndex = MessageIndex(0)

        with open(filePath, 'r') as fd:
            obj.users = reduce(
                __createUserObject__, __groupify__(
                    __splitByDate__(__getRegex__(), fd.read())), [])

        return obj


if __name__ == '__main__':
    print('[!]This module is designed to be used as a backend handler')
    exit(0)
