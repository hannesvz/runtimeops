import json
import sys
from threading import Thread

import flask
import flask.json
import gevent.pywsgi
import pymysql
import requests
from flask import request
from loguru import logger as logging
from platformshconfig import Config

import db

config = Config()

app = flask.Flask(__name__)

mysql_pool = db.get_mysql_pool()


@app.route("/")
def root():
    logging.debug("hit received on /")
    return "now this is podracing!"


if __name__ == "__main__":
    logging.info("starting server")
    db.init_db(mysql_pool)
    http_server = gevent.pywsgi.WSGIServer(("127.0.0.1", int(config.port)), app)
    http_server.serve_forever()
