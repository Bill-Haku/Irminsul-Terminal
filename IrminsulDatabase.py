import datetime

import pymysql
import os
import logging
import time
from botpy.ext.cog_yaml import read

config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))
_log = logging.getLogger('discord')
logHandler = logging.FileHandler(filename='irminsul.log', encoding='utf-8', mode='w')
_log.addHandler(logHandler)


def bindUID(user_id, uid):
    db = pymysql.connect(host=config["host"],
                         user=config["user"],
                         password=config["password"],
                         database=config["database"])
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
        _log.error(f"DB: Bind {user_id} to {uid} FAILED with {e}")
        try:
            db.rollback()
            res = False
        except Exception as ee:
            _log.error(f"DB: Rollback error: {ee}")
            res = False
    db.close()
    return res


def setLanguage(user_id, language):
    db = pymysql.connect(host=config["host"],
                         user=config["user"],
                         password=config["password"],
                         database=config["database"])
    cursor = db.cursor()
    sql = f"""
    update UID_TABLE
    set language = '{language}'
    where user_id = '{user_id}';"""
    checkUIDExist, _, _ = lookUpUID(user_id)
    if not checkUIDExist:
        return False
    try:
        cursor.execute(sql)
        db.commit()
        res = True
        _log.info(f"DB: Set {user_id} language to {language} SUCCESS")
    except Exception as e:
        db.rollback()
        res = False
        _log.error(f"DB: Set {user_id} language to {language} FAILED with {e}")
    db.close()
    return res


def setUpdateTime(user_id, updateTime: datetime.datetime):
    db = pymysql.connect(host=config["host"],
                         user=config["user"],
                         password=config["password"],
                         database=config["database"])
    cursor = db.cursor()
    updateTime.strftime('%Y-%m-%d %H:%M:%S')
    sql = f"""
    update UID_TABLE
    set update_time = '{updateTime}'
    where user_id = '{user_id}';"""
    checkUIDExist, _, _ = lookUpUID(user_id)
    if not checkUIDExist:
        return False
    try:
        cursor.execute(sql)
        db.commit()
        res = True
        _log.info(f"DB: Set {user_id} updateTime SUCCESS")
    except Exception as e:
        db.rollback()
        res = False
        _log.error(f"DB: Set {user_id} updateTime FAILED with {e}")
    db.close()
    return res


def lookUpUID(user_id):
    db = pymysql.connect(host=config["host"],
                         user=config["user"],
                         password=config["password"],
                         database=config["database"])
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
    finally:
        db.close()


def lookUpLanguage(user_id):
    db = pymysql.connect(host=config["host"],
                         user=config["user"],
                         password=config["password"],
                         database=config["database"])
    cursor = db.cursor()
    sql = f"""
    select * from UID_TABLE
    where user_id = '{user_id}';"""
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            language = row[3]
        return True, language

    except Exception as e:
        _log.warning(e)
        return False, ""
    finally:
        db.close()
