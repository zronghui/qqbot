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

allowlist_key = 'shop_allowlist'
denylist_key = 'shop_denylist'
help_str = '''
1. 获得所有白名单 cmd1
2. 添加白名单 cmd2 keyword
3. 删除白名单 cmd3 keyword
4. 获得所有黑名单 cmd4
5. 添加黑名单 cmd5 keyword
6. 删除黑名单 cmd6 keyword
0. 获得帮助 ?
'''


@bot.on_message
def handle_msg(event):
    if event['user_id'] == 825503975 and '已打卡' in event['message']:
        out_message = redis_keywords.miguPunchIn()
        bot.send(event, message=out_message, user_id='825503975')

    message = event['message']
    ic(message, type(message))
    allowlist = redis_keywords.get_keywords(key=allowlist_key)
    denylist = redis_keywords.get_keywords(key=denylist_key)
    group_id = None

    if message in ['?', '？']:
        out_message = help_str
    elif message == 'cmd1':
        out_message = allowlist_key + ':\n' + ' '.join(allowlist)
    elif message.startswith('cmd2 '):
        out_message = redis_keywords.add_keyword(key=allowlist_key,
                                                 keyword=message[4:])
    elif message.startswith('cmd3 '):
        out_message = redis_keywords.rem_keyword(key=allowlist_key,
                                                 keyword=message[4:])
    elif message == 'cmd4':
        out_message = denylist_key + ':\n' + ' '.join(denylist)
    elif message.startswith('cmd5 '):
        out_message = redis_keywords.add_keyword(key=denylist_key,
                                                 keyword=message[4:])
    elif message.startswith('cmd6 '):
        out_message = redis_keywords.rem_keyword(key=denylist_key,
                                                 keyword=message[4:])
    else:
        for deny in denylist:
            if deny in message:
                return
        for allow in allowlist:
            if allow in message:
                out_message = f'关键词:{allow}\n{message}'
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
