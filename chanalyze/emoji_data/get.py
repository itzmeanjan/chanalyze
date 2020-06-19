#!/usr/bin/python3

from __future__ import annotations
from os import getenv
from os.path import (
    join,
    dirname,
    abspath
)
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


def _getEmojiData(url: str = 'https://unicode.org/Public/emoji/12.0/emoji-data.txt') -> List[int]:
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
        # without custom headers remote was blocking request, thinking it's a bot
        resp = getContent(url, headers={
            'Accept': 'text/html,application/xhtml+xml,application/xml,application/json;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:60.0) Gecko/20100101 Firefox/71.0'
        })
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


def exportToFile(sink: str = 'emoji.txt') -> List[int]:
    '''
        Utility function to generate a text file
        containing all supported emojis ( as per Unicode v12.0 )
        along with their corresponding numeric form ( integer value )

        Example :

        .
        .
        .
        11088,⭐
        11093,⭕
        12336,〰
        12349,〽
        .
        .
        .
    '''

    try:
        data = _getEmojiData()
        with open(abspath(join(dirname(__file__), '..', sink)), 'w') as fd:
            fd.writelines(
                map(lambda e: '{},{}\n'.format(e, chr(e)), data))
        return data
    except Exception:
        return None


def importFromFile(source: str = 'emoji.txt') -> List[int]:
    '''
        Given path to emoji file, imports unicode unsigned integer data,
        representing emojis, which can be used for generating plots
    '''

    try:
        with open(abspath(join(dirname(__file__), '..', source)),
                  'r') as fd:
            return list(map(lambda e: int(e.split(',')[0], base=10),
                            fd.readlines()))
    except Exception:
        return None


if __name__ == '__main__':
    print('[!]This module is designed to be used as a backend handler')
    exit(0)
