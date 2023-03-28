import os
import json
import logging

import pymysql
from pymysqlpool.pool import Pool

from platformshconfig import Config
config = Config()

import constant

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=config.variable('LOG_LEVEL', 'DEBUG'))


def init_db(mysql_pool):
    # iterate through list of table and check if they exist - if not, create them
    for table in constant.database_definitions:
        table_name = table['name']
        create_sql = table['sql']
        read_sql = f'SELECT table_name FROM information_schema.tables WHERE table_schema = "main" AND TABLE_NAME = "{table_name}"'
        success,res = query(mysql_pool, read_sql)
        if not success:
            logging.error('Error encountered reading from database - investigate immediately!')

        if success and len(res) != 1:
            logging.error(f'Database read but no "{table_name}" table - creating it!')
            success,res = query(mysql_pool, create_sql)
        if not success:
            logging.error(f'Error encountered creating {table_name} table in database - investigate immediately!')


def get_mysql_pool():
    try:
        credentials = config.credentials('database')
        pool = Pool(
            host=credentials['host'],
            port=credentials['port'],
            db=credentials['path'],
            user=credentials['username'],
            password=credentials['password'],
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        return pool
    except Exception as e:
        logging.error(e)
        return None


def query(pool, sql, data=None):
    try:
        pool.init()

        conn = pool.get_conn()
        cur = conn.cursor()

        result = None
        if data:
            logging.debug(data)
            if type(data) == list:
                cur.executemany(sql, (data))
            else:
                cur.execute(sql, (data))
        else:
            cur.execute(sql)
        result = cur.fetchall()
        cur.close()

    except Exception as e:
        logging.error(e)
        conn.close()
        return False,e

    else:
        logging.debug(f'db query "{sql}" completed successfully')
        conn.close()
        return True,result
