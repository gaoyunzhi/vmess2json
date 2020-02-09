#!/usr/bin/env python3
import os
import sys
import json
import base64
import random

vmscheme = "vmess://"
telegram_proxy = "https://t.me/proxy"
vmess_results = set()
telegram_results = set()

def parseVmess(vmesslink):
    bs = vmesslink[len(vmscheme):]
    blen = len(bs)
    if blen % 4 > 0:
        bs += "=" * (4 - blen % 4)
    vms = base64.b64decode(bs).decode()
    return json.loads(vms)

def toParagraph(vmess):
    return '''地址 (Address) = %s
端口 (Port) = %s
用户ID (User ID / UUID) = %s
额外ID (Alter Id) = %s''' % (vmess['host'], vmess['port'], vmess['id'], vmess['aid'])


def process(item):
    if item.startswith(vmscheme):
        try:
            vmess_results.add(toParagraph(parseVmess(item)))
        except Exception as e:
            return
    if item.startswith(telegram_proxy):
        telegram_results.add(item)

for subdir, dirs, files in os.walk('data'):
    for file in files:
        filepath = subdir + os.sep + file
        with open(filepath) as f:
            for line in f.readlines():
                for item in line.split():
                    process(item)

S1 = '请在各个平台（mac/windows/linus, ios/andriod）安装V2Ray之后输入以下配置，即可登录谷歌，脸书，油管等网站。\n'
S2 = '以下是一些Telegram上的proxy，也欢迎用：'
# This is all ok to commit, not commited by mistake.
S3 = '''\n如果您不想安装app 用电脑端想翻墙的话，可用网页型翻墙，站点如下：
https://misty-disk-50cc.networkfreedom.workers.dev/
https://green-credit-9e7f.networkfreedom.workers.dev/
https://lucky-mountain-6e91.networkfreedom.workers.dev/

设置成功后，欢迎来：
Telegram群：https://t.me/dushufenxiang_chat
Facebook读书群：https://www.facebook.com/groups/reading.sharing/
电子书网站：https://readmoo.com （我的账号是bajie90@gmail.com，密码是dushufenxiang，欢迎大家共用这个账号读书。）

节点由 https://t.me/cnhumanright99, https://t.me/jianjiaobuluo 等提供。'''
result = [S1]
count = 0
for item in random.sample(vmess_results, min(10, len(vmess_results))):
    count += 1
    result.append('设置' + str(count) + ':\n' + item + '\n')
result.append(S2)
result += random.sample(telegram_results, min(10, len(telegram_results)))
result.append(S3)
print('\n'.join(result))