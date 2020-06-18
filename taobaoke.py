import time
import urllib
import hashlib
import urllib.parse
import urllib.request
import json
import re
from icecream import ic


# 挖井人: [python 淘宝OPEN API 调用示例 - 简书](https://www.jianshu.com/p/f9b5e3020789)

# 这里填写你申请到的APPkey
app_key = '30313029'
appSecret = 'afe1d5a676c4f3473e7fa5b8a27a0ade'
user_id = '116455956'
# user_id = '2649229048'


def ksort(d):
    # 排序
    return [(k, d[k]) for k in sorted(d.keys())]


def md5(s, raw_output=False):
    # MD5加密
    """Calculates the md5 hash of a given string"""
    res = hashlib.md5(s.encode())
    if raw_output:
        return res.digest()
    return res.hexdigest()


def createSign(paramArr):
    # 计算sign
    sign = appSecret
    paramArr = ksort(paramArr)
    paramArr = dict(paramArr)
    for k, v in paramArr.items():
        if k != '' and v != '':
            sign += k + v
    sign += appSecret
    sign = md5(sign).upper()
    return sign


def createStrParam(paramArr):
    # 参数排序
    strParam = ''
    for k, v in paramArr.items():
        if k != '' and v != '':
            strParam += k + '=' + urllib.parse.quote_plus(v) + '&'
    return strParam


def gxapi(text, url):
    # 高效API调用示例

    # 请求参数，根据API文档修改
    postparm = {
        'user_id': user_id,
        'text': text,
        'url': url,
        'ext': '{}',
        'method': 'taobao.tbk.tpwd.create'
    }
    # 公共参数，一般不需要修改
    paramArr = {'app_key': app_key,
                'v': '2.0',
                'sign_method': 'md5',
                'format': 'json',
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
                }

    paramArr = {**paramArr, **postparm}

    sign = createSign(paramArr)
    strParam = createStrParam(paramArr)
    strParam += 'sign=' + sign
    url = 'http://gw.api.taobao.com/router/rest?' + strParam
    res = urllib.request.urlopen(url).read()
    return res


def convert(s: str) -> str:
    code = getCode(s)
    url = getUrl(s)
    if not code or not url:
        return s + '\n 不包含 taobao code or taobao url'
    res = gxapi('￥b77k1uAbAqD￥', url='https://s.click.taobao.com/WSZ6Zzu')
    try:
        newcode = json.loads(res)['tbk_tpwd_create_response']['data']['model']
        s = s.replace(code, newcode)
        ic(code, newcode, s)
        return s + '\n 已经替换为张荣辉的 code'
    except Exception as e:
        return s + '\n 获取新的 code 失败：\n' + str(e)
    return s


def getCode(s: str) -> str:
    findres = re.findall(r'￥.*?￥', s)
    if findres:
        return findres[0]
    return ''


def getUrl(s: str) -> str:
    findres = re.findall(r'https://s.click.taobao.com/\w*', s)
    if findres:
        return findres[0]
    return ''


if __name__ == '__main__':
    res = gxapi('￥b77k1uAbAqD￥', url='https://s.click.taobao.com/WSZ6Zzu')
    print(res)
    print(json.loads(res)['tbk_tpwd_create_response']['data']['model'])
    s = '''
    关键词:坚果
【商品】【第二件1元】夏威夷果奶油味坚果
【原价】71.6
【券后价】16.80
【淘口令】￥b77k1uAbAqD￥
【抢券下单】https://s.click.taobao.com/WSZ6Zzu
【推荐】精挑细选，自然馈赠，饱满圆润，奶香四溢，入口爽滑，香脆可口，齿颊留香，自然果香，营养美味，满足你的挑剔味蕾！【赠运费险】
    '''
    assert getCode(s) == '￥b77k1uAbAqD￥'
    assert getUrl(s) == 'https://s.click.taobao.com/WSZ6Zzu'
    print(convert(s))
