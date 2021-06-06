#! /usr/bin/env python

import logging

from flask import Flask
from flask_redis import FlaskRedis

app = Flask(__name__)
app.config.from_pyfile('config.py')

redis_db0 = FlaskRedis(app)

import switch2.sites
import switch2.load_data
import switch2.produce


if __name__ == '__main__':
    app.run()
