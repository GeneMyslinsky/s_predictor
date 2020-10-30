#!/usr/bin/env python
# coding: utf-8

import redis as r
from json import loads,dumps
r = r.Redis(host='redis', port=6379, db=0)


def rpush(key,objects):
    return r.rpush(key,*[dumps(item) for item in objects])
    
def lrange(key):
    return [loads(item) for item in r.lrange(key,0,-1)]

def lpop(key):
    try:
        item = None
        item = loads(r.lpop(key))
    finally: return item
