import requests
import logging


_log = logging.getLogger('discord')
logHandler = logging.FileHandler(filename='irminsul.log', encoding='utf-8', mode='w')
_log.addHandler(logHandler)

ayakaNames = ["10000002", "ayaka", "kamisatoayaka", "绫华", "神里绫华", "神里凌华", "凌华", "綾華", "神里綾華", "神里綾香", "綾香"]
hutaoNames = ["10000046", "hutao", "胡桃", "胡桃"]

locResponse = requests.get("http://ophelper.top/api/players/loc.json")
locResult = locResponse.json()

def charName2IDConverter(name):
    name = name.lower()
    if name in ayakaNames:
        return 10000002
    elif name in hutaoNames:
        return 10000046
    else:
        return 0


def charFullName(charID, language):
    charResponse = requests.get("http://ophelper.top/api/players/characters.json")
    charResult = charResponse.json()
    nameTextMapHash = charResult[f"{charID}"]["NameTextMapHash"]
    locResponse = requests.get("http://ophelper.top/api/players/loc.json")
    locResult = locResponse.json()

    if language == "zh":
        language = "zh-CN"
    return locResult[f"{language}"][f"{nameTextMapHash}"]


def textMapHash2Text(nameTextMapHash, language):

    if language == "zh":
        language = "zh-CN"

    try:
        res = locResult[f"{language}"][f"{nameTextMapHash}"]
    except Exception as e:
        _log.warning(f"find text {nameTextMapHash} fail: {e}")
        res = nameTextMapHash
    return res

