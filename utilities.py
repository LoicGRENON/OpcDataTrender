# coding=utf-8

import datetime
import time


def getTimestamp():
    return time.mktime(datetime.datetime.now().timetuple())
