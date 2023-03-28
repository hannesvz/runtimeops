import json
import sys
import logging
import requests

import flask
import flask.json
import gevent.pywsgi
import pymysql
import slack

from flask import request
from threading import Thread

from platformshconfig import Config
config = Config()

app = flask.Flask(__name__)

logging.basicConfig(format='%(asctime)s {%(pathname)s:%(lineno)d} %(levelname)s %(message)s', level=config.variable('LOG_LEVEL', 'DEBUG'))


@app.route('/')
def root():
    return 'now this is podracing!'


if __name__ == "__main__":
    http_server = gevent.pywsgi.WSGIServer(('127.0.0.1', int(config.port)), app)
    http_server.serve_forever()
