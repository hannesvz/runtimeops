import base64
import os
import datetime
import random
import logging

import db

from platformshconfig import Config
config = Config()

logging.basicConfig(format='%(asctime)s {%(pathname)s:%(lineno)d} %(levelname)s %(message)s', level=config.variable('LOG_LEVEL', 'DEBUG'))

mysql_pool = db.get_mysql_pool()

if __name__ == "__main__":
    req_id = base64.b32encode(os.urandom(16)).lower().strip(b"=").decode("utf-8")[:13]
    secret = random.random()
    logging.debug(f'inserting record {req_id}...')
    db_success,db_res = db.query(mysql_pool, f"insert into `main`.`records` ('req_id', 'secret', 'created') values ( {req_id}, {secret}, DEFAULT(created) )")
    if db_success:
        logging.debug(f'{req_id} inserted!')
    else:
        logging.error(f'error writing record {req_id}!')
