import datetime
import json
import requests
import os
import logging

import IrminsulDatabase

_log = logging.getLogger('discord')
logHandler = logging.FileHandler(filename='irminsul.log', encoding='utf-8', mode='w')
_log.addHandler(logHandler)


def getEnkaAPIResult(uid):
    fileName = f"./userEnkaData/{uid}.json"
    try:
        with open(fileName) as enkaDataLocalFile:
            enkaData = json.load(enkaDataLocalFile)
            return enkaData
    except OSError as e:
        # no file found
        _log.info(f"failed to find data of {uid} at local, get from enka")
        enkaData = getDataFromEnka(uid)
        return enkaData


def getDataFromEnka(uid):
    headers = {"User-Agent": "Project Irminsul Terminal/1.0"}
    response = requests.get(f"https://enka.network/u/{uid}/__data.json", headers=headers)
    result = response.json()
    # save data into files
    if not os.path.exists("userEnkaData"):
        os.mkdir("userEnkaData")
    filename = f"./userEnkaData/{uid}.json"
    with open(filename, "w") as obj:
        json.dump(result, obj)
    return result


def updateDataFromEnka(userId, uid, updateTime, i18n):
    now = datetime.datetime.now().astimezone()
    updateTime = updateTime.astimezone()
    timeDelta = now - updateTime
    if timeDelta.seconds <= 120:
        return False, i18n["msg.error.enkaUpdateTooFast"]
    enkaData = getDataFromEnka(uid)
    playerInfo = None
    try:
        playerInfo = enkaData["playerInfo"]
    except KeyError:
        return False, i18n["msg.error.enkaUpdateFail"]

    if enkaData is not None and playerInfo is not None:
        res = IrminsulDatabase.setUpdateTime(user_id=userId, updateTime=now)
        if res:
            return True, ""
        else:
            return False, i18n["msg.error.enkaUpdateFail"]
    else:
        return False, i18n["msg.error.enkaUpdateFail"]
