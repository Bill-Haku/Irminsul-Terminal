import pymysql
import os
import logging
from botpy.ext.cog_yaml import read

config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))
_log = logging.getLogger('discord')
logHandler = logging.FileHandler(filename='irminsul.log', encoding='utf-8', mode='w')
_log.addHandler(logHandler)

db = pymysql.connect(host=config["host"],
                     user=config["user"],
                     password=config["password"],
                     database=config["database"])


def bindUID(user_id, uid):
    cursor = db.cursor()
    sql = f"""
    insert into UID_TABLE(user_id, uid, update_time)
    values ('{user_id}', '{uid}', now())
    on duplicate key update uid = '{uid}', update_time = now();"""
    try:
        cursor.execute(sql)
        db.commit()
        res = True
        _log.info(f"DB: Bind {user_id} to {uid} SUCCESS")
    except Exception as e:
        db.rollback()
        res = False
        _log.error(f"DB: Bind {user_id} to {uid} FAILED with {e}")

    db.close()
    return res


def lookUpUID(user_id):
    cursor = db.cursor()
    sql = f"""
    select * from UID_TABLE
    where user_id = '{user_id}';"""
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            uid = row[1]
            updateTime = row[2]
        return True, uid, updateTime

    except Exception as e:
        _log.warning(e)
        return False, "", ""

