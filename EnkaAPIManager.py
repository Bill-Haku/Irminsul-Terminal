import json
import requests


def getEnkaAPIResult(uid):
    fileName = f"./userEnkaData/{uid}.json"
    try:
        with open(fileName) as enkaDataLocalFile:
            enkaData = json.load(enkaDataLocalFile)
            return enkaData
    except OSError as e:
        # no file found
        enkaData = getDataFromEnka(uid)
        return enkaData


def getDataFromEnka(uid):
    headers = {"User-Agent": "Project Irminsul Terminal/1.0"}
    response = requests.get(f"https://enka.network/u/{uid}/__data.json", headers=headers)
    result = response.json()
    # save data into files
    filename = f"./userEnkaData/{uid}.json"
    with open(filename, "w") as obj:
        json.dump(result, obj)
    return result
