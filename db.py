import json
import os

import pymysql
from loguru import logger as logging
from platformshconfig import Config
from pymysqlpool.pool import Pool

config = Config()

import constant


def init_db(mysql_pool):
    # iterate through list of table and check if they exist - if not, create them
    for table in constant.database_definitions:
        table_name = table["name"]
        create_sql = table["sql"]
        read_sql = f'SELECT table_name FROM information_schema.tables WHERE table_schema = "main" AND TABLE_NAME = "{table_name}"'
        success, res = query(mysql_pool, read_sql)
        if not success:
            logging.error(
                "Error encountered reading from database - investigate immediately!"
            )

        if success and len(res) != 1:
            logging.error(f'Database read but no "{table_name}" table - creating it!')
            success, res = query(mysql_pool, create_sql)
        if not success:
            logging.error(
                f"Error encountered creating {table_name} table in database - investigate immediately!"
            )


def get_mysql_pool():
    try:
        credentials = config.credentials("database")
        pool = Pool(
            host=credentials["host"],
            port=credentials["port"],
            db=credentials["path"],
            user=credentials["username"],
            password=credentials["password"],
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True,
        )
        return pool
    except Exception as e:
        logging.error(e)
        return None


def query(pool, sql, data=None):
    logging.debug(f"executing sql query {sql}. current pool size: {pool.current_size}")
    try:
        # loop forever until a db connection can be obtained
        while True:
            try:
                conn = pool.get_conn()
                cur = conn.cursor()
                break
            except:
                logging.debug(f"Could not get sql pool connection. Waiting 1 second...")
                time.sleep(1)
                pass

        result = None

        if data:
            logging.debug(data)
            if type(data) == list:
                cur.executemany(sql, data)
            else:
                cur.execute(sql, data)
        else:
            cur.execute(sql)

        result = cur.fetchall()

    except Exception as e:
        logging.error(f"exception raised during main try block - {str(e)}")
        return False, e

    try:
        logging.debug(f"closing connection. current pool size: {pool.current_size}")
        pool.release(conn)
        logging.debug(f"connection closed. current pool size: {pool.current_size}")
    except Exception as e:
        logging.error(f"Error encountered releasing the pool connection: {str(e)}")
        pass

    logging.debug(f'db query "{sql}" completed successfully')
    return True, result
