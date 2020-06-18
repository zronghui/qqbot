#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pretty_errors
import redis

pretty_errors.activate()
host = '127.0.0.1'
port = 6379
r = redis.StrictRedis(host=host, port=port)


def get_keywords() -> list:
    return [i.decode("utf-8") for i in r.smembers('keywords')]


def add_keyword(keyword: str) -> str:
    keyword = keyword.strip()
    if r.sadd('keywords', keyword) == 1:
        out_message = '插入\'' + keyword + '\'成功'
    else:
        out_message = '插入\'' + keyword + '\'失败'
    return out_message


def rem_keyword(keyword: str) -> str:
    keyword = keyword.strip()
    if r.srem('keywords', keyword) == 1:
        out_message = '删除\'' + keyword + '\'成功'
    else:
        out_message = '删除\'' + keyword + '\'失败'
    return out_message


if __name__ == '__main__':
    print(add_keyword('1 2'))
    print(rem_keyword('1 2'))
    print(get_keywords())
