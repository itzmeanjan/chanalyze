#!/usr/bin/python3

from requests import get as getContent
from re import compile as regCompile
from functools import reduce
from typing import List

'''
    Designed to extract out all supported
    emojis from Unicode.org ( 1311 in count, as per v12.0 )

    Takes a target url ( from where it'll fetch these data ),
    though a default value is provided, may be when next version 
    of unicode releases, I'll update default value.

    Returns all supported emojis as List[int]
'''


def getEmojiData(url: str = 'https://unicode.org/Public/emoji/12.0/emoji-data.txt') -> List[int]:
    '''
        There're certain cases where a code can be given
        in following form

        `xxxx..xxxx`

        For covering all values hiding in that
        range, I wrote following utility funtion,
        which will returns a List[int], holding
        all those values, which will eventually be
        appended to accumulated List[int]
    '''
    def __split__(e: str) -> List[int]:
        return [i for i in range(*[(int(j, base=16) + 1) if i == 1 else int(j, base=16)
                                   for i, j in enumerate(e.split('..'))])]
    try:
        resp = getContent(url)
        if not resp.ok:
            raise Exception('Bad Response from Remote')
        # regex to filter out lines which are having emojis listed
        regEmoji = regCompile(
            r'^[0-9A-F]{4,}([\.\.0-9A-F]+)?\s+;\s*Emoji\s+\#.+$')
        regHexCode = regCompile(r'^[0-9A-F]{4,}(\S+)?(?=\s+;)')
        return reduce(
            lambda acc, cur: acc +
            __split__(cur) if '..' in cur else acc + [int(cur, base=16)],
            map(lambda e: regHexCode.search(e).group(),
                filter(lambda e:
                       (not e.startswith('#')) and regEmoji.search(e),
                       resp.content.decode('utf-8').splitlines())), [])
    except Exception:
        return None


if __name__ == '__main__':
    print('[!]This module is designed to be used as a backend handler')
    exit(0)
