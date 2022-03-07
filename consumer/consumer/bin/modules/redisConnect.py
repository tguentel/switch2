#!/usr/bin/env python

import redis

def read(key, host, port, redisdb):
    pool = redis.ConnectionPool(host=host, port=port, db=redisdb)
    rcon = redis.Redis(connection_pool=pool)
    result = rcon.get(key)
    return result

