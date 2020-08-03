#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pretty_errors
import redis
from datetime import datetime

pretty_errors.activate()
host = '127.0.0.1'
port = 6379
r = redis.StrictRedis(host=host, port=port)


def get_keywords(key) -> list:
    return [i.decode("utf-8") for i in r.smembers(key)]


def add_keyword(key, keyword: str) -> str:
    keyword = keyword.strip()
    if r.sadd(key, keyword) == 1:
        out_message = key + ' 插入\'' + keyword + '\'成功'
    else:
        out_message = key + ' 插入\'' + keyword + '\'失败'
    return out_message


def rem_keyword(key, keyword: str) -> str:
    keyword = keyword.strip()
    if r.srem(key, keyword) == 1:
        out_message = key + ' 删除\'' + keyword + '\'成功'
    else:
        out_message = key + ' 删除\'' + keyword + '\'失败'
    return out_message


def miguPunchIn():
    today = datetime.today().strftime('%Y-%m-%d')
    if r.sadd('migudays', today) == 1:
        out_message = '打卡成功'
    else:
        out_message = '打卡失败'
    return out_message


def miguPunched():
    today = datetime.today().strftime('%Y-%m-%d')
    return r.sismember('migudays', today)
    # if r.sismember('migudays', today):
    #     return '今日已打卡'
    # return '今日未打卡'


def miguDays():
    return str(r.scard('migudays'))


if __name__ == '__main__':
    print(add_keyword('1 2'))
    print(rem_keyword('1 2'))
    print(get_keywords())
