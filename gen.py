#!/usr/bin/env python3
import os
import sys
import json
import base64
import random

vmscheme = "vmess://"
telegram_proxy = "https://t.me/proxy"
vmess_results = []
telegram_results = []

def parseVmess(vmesslink):
    bs = vmesslink[len(vmscheme):]
    blen = len(bs)
    if blen % 4 > 0:
        bs += "=" * (4 - blen % 4)
    vms = base64.b64decode(bs).decode()
    return json.loads(vms)

def process(item):
    if item.startswith(vmscheme):
        try:
            return vmess_results.append(parseVmess(item))
        except:
            return
    if item.startswith(telegram_proxy):
        telegram_results.append(item)

for subdir, dirs, files in os.walk('data'):
    for file in files:
        filepath = subdir + os.sep + file
        with open(filepath) as f:
            for line in f.readlines():
                for item in line.split():
                    process(item)

print(vmess_results)
print(telegram_results)