#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pretty_errors
from cqhttp import CQHttp
from icecream import ic
import schedule
import time

pretty_errors.activate()

bot = CQHttp(api_root='http://127.0.0.1:5700/',
             # access_token='your-token',
             # secret='your-secret'
             )


def miguNotify():
    message = '咪咕打卡'
    bot.send(event={}, message=message, user_id='825503975')


schedule.every(15).minutes.do(miguNotify)

while True:
    schedule.run_pending()
    time.sleep(1)
