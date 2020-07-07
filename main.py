#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pretty_errors
from cqhttp import CQHttp
from icecream import ic


import redis_keywords
# import taobaoke

pretty_errors.activate()
bot = CQHttp(api_root='http://127.0.0.1:5700/',
             # access_token='your-token',
             # secret='your-secret'
             )


@bot.on_message
def handle_msg(event):
    if event['user_id'] == 825503975 and '已打卡' in event['message']:
        out_message = redis_keywords.miguPunchIn()
        bot.send(event, message=out_message, user_id='825503975')

    message = event['message']
    ic(message, type(message))
    keywords = redis_keywords.get_keywords()
    group_id = None

    if message in ['?', '？']:
        out_message = '1. 获得所有关键词 cmd1\n2. 添加关键词 cmd2 keyword\n3. 删除关键词 cmd3 keyword\n4. 获得帮助 ?'
    elif message == 'cmd1':
        out_message = ' '.join(keywords)
    elif message.startswith('cmd2 '):
        out_message = redis_keywords.add_keyword(message[4:])
    elif message.startswith('cmd3 '):
        out_message = redis_keywords.rem_keyword(message[4:])
    else:
        for keyword in keywords:
            if keyword in message:
                out_message = f'关键词:{keyword}\n{message}'
                # out_message = taobaoke.convert(out_message)
                group_id = '1103014124'
                break
        else:
            out_message = ''
    if out_message != '':
        ic(out_message)
        if group_id:
            bot.send(event, message=out_message, group_id=group_id)
        else:
            bot.send(event, message=out_message)


@bot.on_request('group', 'friend')
def handle_request(event):
    return {'approve': True}  # 同意所有加群、加好友请求


# @bot.on_message
# def miguPunchIn(event):
#     # ic(event['sender'], event['user_id'], event['message'])
#     if event['user_id'] == 825503975 and '已打卡' in event['message']:
#         out_message = redis_keywords.miguPunchIn()
#         bot.send(event, message=out_message, user_id='825503975')


bot.run(host='0.0.0.0', port=4991, debug=True)
