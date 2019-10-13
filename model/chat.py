#!/usr/bin/python3

from typing import List, Tuple
from re import compile as reg_compile, Pattern
from functools import reduce
from sys import path
from os.path import abspath, dirname
try:
    path.append(dirname(abspath(__file__)))
    from message import Message, MessageIndex
    from user import User
except ImportError as e:
    print('[!]Module Unavailable : {}'.format(str(e)))
    exit(1)

'''
    A whole chat, which is generally exported into a text file ( *.txt )
    from WhatsApp, is read and processed & converted into Chat object.
'''


class Chat(object):
    _messageCount = 0

    def __init__(self, users):
        self.users = users

    '''
        Returns calculated # of messages present in this chat
    '''
    @property
    def messageCount(self) -> int:
        return sum([len(i.messages) for i in self.users])

    '''
        Finds out whether a certain User participated in this chat or not
        ( by its name )

        In case of failure, returns None
    '''

    def getUser(self, name: str):
        return reduce(lambda acc, cur: cur if cur.name ==
                      name else acc, self.users, None)

    @staticmethod
    def importFromText(filePath: str):
        '''
            Regex to be used for extracting timestamp of
            a certain message from `*.txt` file
        '''
        def __getRegex__() -> Pattern:
            return reg_compile(
                r'(\d{1,2}/\d{1,2}/\d{2}, \d{1,2}\:\d{1,2} [a|p]m)')

        '''
            splitting whole *.txt file content using
            date extraction regex we just built
        '''
        def __splitByDate__(pattern: Pattern, content: str) -> List[str]:
            return pattern.split(content)[1:]

        '''
            In previous closure we splitted whole text file content by date,
            which needs to be fixed by pairing messages with its corresponding timestamp
        '''
        def __groupify__(splitted: List[str]) -> List[Tuple[str, str]]:
            grouped = []
            for i in range(0, len(splitted), 2):
                grouped.append((splitted[i], splitted[i+1]))
            return grouped

        '''
            Helps in extracting participating user name from message ( text )
        '''
        def __getUser__(text: str) -> str:
            matchObj = reg_compile(r'(?<=\s-\s).+?(?=:)').search(text)
            return matchObj.group() if matchObj else ''

        '''
            Extracts actual message sent by a certain user using regex
        '''
        def __getMessage__(text: str) -> str:
            return reg_compile(r'\s-\s.+?(?=:):\s*').sub('', text)

        '''
            Construction of User objects ( who participated in chat ) along with
            messages sent by them, done in this closure
        '''
        def __createUserObject__(acc, content: Tuple[str, str]):
            # if we can't extract username from message text, it's not a message of this chat, so we just ignore it
            userName = __getUser__(content[1])
            if not userName:
                return acc  # returning in unchanged form
            msg = Message(msgIndex.index, __getMessage__(
                content[1]), content[0])
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
        try:
            msgIndex = MessageIndex(0)
            with open(filePath, 'r') as fd:
                obj.users = reduce(
                    __createUserObject__, __groupify__(
                        __splitByDate__(__getRegex__(), fd.read())), [])
        except Exception:
            obj = None
        finally:
            return obj


if __name__ == '__main__':
    print('[!]This module is designed to be used as a backend handler')
    exit(0)
