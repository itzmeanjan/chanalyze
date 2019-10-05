#!/usr/bin/python3

from __future__ import annotations
from typing import List, Tuple
from re import compile as reg_compile, Pattern
try:
    from user import User
except ImportError as e:
    print('[!]Module Unavailable : {}'.format(str(e)))
    exit(1)


class Chat(object):
    def __init__(self, users: List[User]):
        self.users = users

    @staticmethod
    def importFromText(filePath: str) -> Chat:
        def __getRegex__() -> Pattern:
            return reg_compile(
                r'(\d{1,2}/\d{1,2}/\d{2}, \d{1,2}\:\d{1,2} [a|p]m)')

        def __splitByDate__(pattern: Pattern, content: str) -> List[str]:
            return pattern.split(content)[1:]

        def __groupify__(splitted: List[str]) -> List[Tuple[str]]:
            grouped = []
            for i in range(0, len(splitted), 2):
                grouped.append((splitted[i], splitted[i+1]))
            return grouped

        def __getUser__(text: str) -> str:
            matchObj = regexUser.search(text)
            return matchObj.group() if matchObj else ''

        obj = None
        try:
            with open(filePath, 'r') as fd:
                messages = __groupify__(
                    __splitByDate__(__getRegex__(), fd.read()))
                regexUser = reg_compile(r'(?<=\s-\s).+(?=:)')
        except Exception:
            obj = None
        finally:
            return obj


if __name__ == '__main__':
    print('[!]This module is designed to be used as a backend handler')
    exit(0)
