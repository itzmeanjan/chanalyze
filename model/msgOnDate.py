#!/usr/bin/python3

from __future__ import annotations
from datetime import date

'''
    Holds # of messages sent on a certain date,
    denoted by dd/mm/yyyy
'''


class MessagesSentOnDate(object):
    def __init__(self, currentDate: date, count: int):
        self.currentDate = currentDate
        self.count = count

    def incrementBy(self, by: int = 1):
        self.count += by


if __name__ == '__main__':
    print('[!]This module is designed to be used as a backend handler')
    exit(0)
