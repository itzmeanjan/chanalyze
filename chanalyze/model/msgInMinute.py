#!/usr/bin/python3

from __future__ import annotations
from typing import List
from datetime import time


class MessagesSentInMinute(object):
    def __init__(self, hour: int, minute: int, count: int):
        self.hour = hour
        self.minute = minute
        self.count = count

    def incrementCount(self, by: int = 1):
        self.count += 1


class MessagesSentInADay(object):
    def __init__(self, records: List[MessagesSentInMinute]):
        self.records = records

    def findARecord(self, findIt: time) -> MessagesSentInMinute:
        return self.records[findIt.hour*60 + findIt.minute]


if __name__ == '__main__':
    print('[!]This module is expected to be used as a backend handler')
    exit(0)
