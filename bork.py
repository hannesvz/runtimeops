import base64
import os
import sys
import datetime
import random
from loguru import logger as logging

import db

from platformshconfig import Config
config = Config()


mysql_pool = db.get_mysql_pool()

if __name__ == "__main__":
    req_id = base64.b32encode(os.urandom(16)).lower().strip(b"=").decode("utf-8")[:13]
    secret = random.random()
    logging.debug(f'inserting record {req_id}...')
    print(f'print equivalent: inserting record {req_id}...', flush=True)
    db_success,db_res = db.query(mysql_pool, f"insert into `main`.`records` (`req_id`, `secret`) values ( '{req_id}', '{secret}' )")
    if db_success:
        logging.debug(f'{req_id} inserted!')
    else:
        logging.error(f'error writing record {req_id}!')
    sys.exit(0)
