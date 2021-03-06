#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pretty_errors
from cqhttp import CQHttp
from icecream import ic
import schedule
import time
import redis_keywords

pretty_errors.activate()

bot = CQHttp(api_root='http://127.0.0.1:5700/',
             # access_token='your-token',
             # secret='your-secret'
             )


# todo: 多个提醒，不同的 message、提醒间隔; 不同提醒的打卡日期放redis 同一个 key 里
def miguNotify():
    message = '咪咕打卡'
    print(redis_keywords.miguDays())
    if not redis_keywords.miguPunched():
        bot.send(event={}, message=message, user_id='825503975')


schedule.every(15).minutes.do(miguNotify)

while True:
    schedule.run_pending()
    time.sleep(1)
