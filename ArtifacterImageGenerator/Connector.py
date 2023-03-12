from typing import Dict, Any

import ArtifacterImageGenerator.Generater as Generater
import CharIDDatabase


def dataConverter(avatarData, fullData, language):
    fightPopMap = avatarData["fightPropMap"]
    # Elemental DMG Bonus
    elementalDmg: dict[str, Any] = {}
    if fightPopMap["40"] != 0:
        elementalDmg.update({"火元素ダメージ": round(fightPopMap['40'] * 100, 2)})
    if fightPopMap["41"] != 0:
        elementalDmg.update({"雷元素ダメージ": round(fightPopMap['41'] * 100, 2)})
    if fightPopMap["42"] != 0:
        elementalDmg.update({"水元素ダメージ": round(fightPopMap['42'] * 100, 2)})
    if fightPopMap["43"] != 0:
        elementalDmg.update({"草元素ダメージ": round(fightPopMap['43'] * 100, 2)})
    if fightPopMap["44"] != 0:
        elementalDmg.update({"風元素ダメージ": round(fightPopMap['44'] * 100, 2)})
    if fightPopMap["45"] != 0:
        elementalDmg.update({"岩元素ダメージ": round(fightPopMap['45'] * 100, 2)})
    if fightPopMap["46"] != 0:
        elementalDmg.update({"氷元素ダメージ": round(fightPopMap['46'] * 100, 2)})
    if fightPopMap["30"] != 0:
        elementalDmg.update({"物理ダメージ": round(fightPopMap['30'] * 100, 2)})

    # talent info
    talentInfo = {}
    talentNameList = ["通常", "スキル", "爆発"]
    talentIndex = 0
    if len(avatarData["skillLevelMap"].keys()) > 3:
        talentIndex -= len(avatarData["skillLevelMap"].keys()) - 3
    for key in avatarData["skillLevelMap"].keys():
        if talentIndex < 0:
            talentIndex += 1
            continue
        talentInfo.update({f"{talentNameList[talentIndex]}": avatarData["skillLevelMap"][key]})
        talentIndex += 1

    # weapon & artifact info
    weaponItem = None
    artifactFlower = {}
    artifactWing = {}
    artifactClock = {}
    artifactCup = {}
    artifactCrown = {}
    artifactScore = {
        "State": "",
        "total": 0.0,
        "flower": 0.0,
        "wing": 0.0,
        "clock": 0.0,
        "cup": 0.0,
        "crown": 0.0
    }
    artifactClockItem = None
    for item in avatarData["equipList"]:
        if "reliquary" in item:
            if item["flat"]["equipType"] == "EQUIP_SHOES":
                artifactClockItem = item

    for item in avatarData["equipList"]:
        if "reliquary" in item:
            if item["flat"]["equipType"] == "EQUIP_BRACER":
                artifactFlower.update({"type": CharIDDatabase.textMapHash2Text(item["flat"]["setNameTextMapHash"],
                                                                               language="ja")})
                artifactFlower.update({"Level": item["reliquary"]["level"] - 1})
                artifactFlower.update({"rarelity": item["flat"]["rankLevel"]})
                artifactFlower.update({"main": {
                    "option": CharIDDatabase.artifactPropNameTranslator(item["flat"]["reliquaryMainstat"]["mainPropId"],
                                                                        language="ja"),
                    "value": item["flat"]["reliquaryMainstat"]["statValue"]
                }})
                artifactFlower.update({"sub": []})
                for subStats in item["flat"]["reliquarySubstats"]:
                    artifactFlower["sub"].append({
                        "option": CharIDDatabase.artifactPropNameTranslator(subStats["appendPropId"],
                                                                            language="ja"),
                        "value": subStats["statValue"]
                    })
                    if subStats["appendPropId"] == "FIGHT_PROP_CRITICAL":
                        artifactScore["flower"] += subStats["statValue"] * 2
                    elif subStats["appendPropId"] == "FIGHT_PROP_CRITICAL_HURT":
                        artifactScore["flower"] += subStats["statValue"]
                    if artifactClockItem is not None:
                        if artifactClockItem["flat"]["reliquaryMainstat"]["mainPropId"] == subStats["appendPropId"]:
                            artifactScore["flower"] += subStats["statValue"] * 0.8
            elif item["flat"]["equipType"] == "EQUIP_NECKLACE":
                artifactWing.update({"type": CharIDDatabase.textMapHash2Text(item["flat"]["setNameTextMapHash"],
                                                                             language="ja")})
                artifactWing.update({"Level": item["reliquary"]["level"] - 1})
                artifactWing.update({"rarelity": item["flat"]["rankLevel"]})
                artifactWing.update({"main": {
                    "option": CharIDDatabase.artifactPropNameTranslator(item["flat"]["reliquaryMainstat"]["mainPropId"],
                                                                        language="ja"),
                    "value": item["flat"]["reliquaryMainstat"]["statValue"]
                }})
                artifactWing.update({"sub": []})
                for subStats in item["flat"]["reliquarySubstats"]:
                    artifactWing["sub"].append({
                        "option": CharIDDatabase.artifactPropNameTranslator(subStats["appendPropId"],
                                                                            language="ja"),
                        "value": subStats["statValue"]
                    })
                    if subStats["appendPropId"] == "FIGHT_PROP_CRITICAL":
                        artifactScore["wing"] += subStats["statValue"] * 2
                    elif subStats["appendPropId"] == "FIGHT_PROP_CRITICAL_HURT":
                        artifactScore["wing"] += subStats["statValue"]
                    if artifactClockItem is not None:
                        if artifactClockItem["flat"]["reliquaryMainstat"]["mainPropId"] == subStats["appendPropId"]:
                            artifactScore["wing"] += subStats["statValue"] * 0.8
            elif item["flat"]["equipType"] == "EQUIP_SHOES":
                artifactClock.update({"type": CharIDDatabase.textMapHash2Text(item["flat"]["setNameTextMapHash"],
                                                                              language="ja")})
                artifactClock.update({"Level": item["reliquary"]["level"] - 1})
                artifactClock.update({"rarelity": item["flat"]["rankLevel"]})
                artifactClock.update({"main": {
                    "option": CharIDDatabase.artifactPropNameTranslator(item["flat"]["reliquaryMainstat"]["mainPropId"],
                                                                        language="ja"),
                    "value": item["flat"]["reliquaryMainstat"]["statValue"]
                }})
                artifactClock.update({"sub": []})
                for subStats in item["flat"]["reliquarySubstats"]:
                    artifactClock["sub"].append({
                        "option": CharIDDatabase.artifactPropNameTranslator(subStats["appendPropId"],
                                                                            language="ja"),
                        "value": subStats["statValue"]
                    })
                    if subStats["appendPropId"] == "FIGHT_PROP_CRITICAL":
                        artifactScore["clock"] += subStats["statValue"] * 2
                    elif subStats["appendPropId"] == "FIGHT_PROP_CRITICAL_HURT":
                        artifactScore["clock"] += subStats["statValue"]
                    if artifactClockItem is not None:
                        if artifactClockItem["flat"]["reliquaryMainstat"]["mainPropId"] == subStats["appendPropId"]:
                            artifactScore["clock"] += subStats["statValue"] * 0.8
            elif item["flat"]["equipType"] == "EQUIP_RING":
                artifactCup.update({"type": CharIDDatabase.textMapHash2Text(item["flat"]["setNameTextMapHash"],
                                                                            language="ja")})
                artifactCup.update({"Level": item["reliquary"]["level"] - 1})
                artifactCup.update({"rarelity": item["flat"]["rankLevel"]})
                artifactCup.update({"main": {
                    "option": CharIDDatabase.artifactPropNameTranslator(item["flat"]["reliquaryMainstat"]["mainPropId"],
                                                                        language="ja"),
                    "value": item["flat"]["reliquaryMainstat"]["statValue"]
                }})
                artifactCup.update({"sub": []})
                for subStats in item["flat"]["reliquarySubstats"]:
                    artifactCup["sub"].append({
                        "option": CharIDDatabase.artifactPropNameTranslator(subStats["appendPropId"],
                                                                            language="ja"),
                        "value": subStats["statValue"]
                    })
                    if subStats["appendPropId"] == "FIGHT_PROP_CRITICAL":
                        artifactScore["cup"] += subStats["statValue"] * 2
                    elif subStats["appendPropId"] == "FIGHT_PROP_CRITICAL_HURT":
                        artifactScore["cup"] += subStats["statValue"]
                    if artifactClockItem is not None:
                        if artifactClockItem["flat"]["reliquaryMainstat"]["mainPropId"] == subStats["appendPropId"]:
                            artifactScore["cup"] += subStats["statValue"] * 0.8
            elif item["flat"]["equipType"] == "EQUIP_DRESS":
                artifactCrown.update({"type": CharIDDatabase.textMapHash2Text(item["flat"]["setNameTextMapHash"],
                                                                              language="ja")})
                artifactCrown.update({"Level": item["reliquary"]["level"] - 1})
                artifactCrown.update({"rarelity": item["flat"]["rankLevel"]})
                artifactCrown.update({"main": {
                    "option": CharIDDatabase.artifactPropNameTranslator(item["flat"]["reliquaryMainstat"]["mainPropId"],
                                                                        language="ja"),
                    "value": item["flat"]["reliquaryMainstat"]["statValue"]
                }})
                artifactCrown.update({"sub": []})
                for subStats in item["flat"]["reliquarySubstats"]:
                    artifactCrown["sub"].append({
                        "option": CharIDDatabase.artifactPropNameTranslator(subStats["appendPropId"],
                                                                            language="ja"),
                        "value": subStats["statValue"]
                    })
                    if subStats["appendPropId"] == "FIGHT_PROP_CRITICAL":
                        artifactScore["crown"] += subStats["statValue"] * 2
                    elif subStats["appendPropId"] == "FIGHT_PROP_CRITICAL_HURT":
                        artifactScore["crown"] += subStats["statValue"]
                    if artifactClockItem is not None:
                        if artifactClockItem["flat"]["reliquaryMainstat"]["mainPropId"] == subStats["appendPropId"]:
                            artifactScore["crown"] += subStats["statValue"] * 0.8
        if "weapon" in item:
            weaponItem = item

    artifactScore["flower"] = round(artifactScore["flower"], 1)
    artifactScore["wing"] = round(artifactScore["wing"], 1)
    artifactScore["clock"] = round(artifactScore["clock"], 1)
    artifactScore["cup"] = round(artifactScore["cup"], 1)
    artifactScore["crown"] = round(artifactScore["crown"], 1)
    artifactScore["total"] = artifactScore["flower"] + artifactScore["wing"] + artifactScore["clock"] + \
                             artifactScore["cup"] + artifactScore["crown"]
    artifactScore["total"] = round(artifactScore["total"], 1)
    artifactScore["State"] = CharIDDatabase.artifactPropNameTranslator(artifactClockItem["flat"]["reliquaryMainstat"]["mainPropId"],
                                                                       language="ja")
    # const
    if "talentIdList" in avatarData:
        const = len(avatarData["talentIdList"])
    else:
        const = 0

    # weapon R
    weaponTotu = 0
    affixMapKeys = weaponItem["weapon"]["affixMap"].keys()
    for affixMapKey in affixMapKeys:
        weaponTotu = weaponItem["weapon"]["affixMap"][affixMapKey] + 1

    data = {
        "uid": fullData["uid"],
        "input": "",
        "Character": {
            "Name": CharIDDatabase.charFullName(charID=avatarData["avatarId"], language="ja"),
            "Const": const,
            "Level": avatarData["propMap"]["4001"]["val"],
            "Love": avatarData["fetterInfo"]["expLevel"],
            "Status": {
                "HP": round(fightPopMap['2000'], 2),
                "攻撃力": round(fightPopMap['2001'], 2),
                "防御力": round(fightPopMap['2002'], 2),
                "元素熟知": round(fightPopMap['28'], 2),
                "会心率": round(fightPopMap['20'] * 100, 2),
                "会心ダメージ": round(fightPopMap['22'] * 100, 2),
                "元素チャージ効率": round(fightPopMap['23'] * 100, 2)
            },
            "Talent": {
            },
            "Base": {
                "HP": round(fightPopMap['1'], 2),
                "攻撃力": round(fightPopMap['4'], 2),
                "防御力": round(fightPopMap['7'], 2)
            }
        },
        "Weapon": {
            "name": CharIDDatabase.textMapHash2Text(weaponItem["flat"]["nameTextMapHash"], language="ja"),
            "Level": weaponItem["weapon"]["level"],
            "totu": weaponTotu,
            "rarelity": weaponItem["flat"]["rankLevel"],
            "BaseATK": weaponItem["flat"]["weaponStats"][0]["statValue"],
            "Sub": {
                "name": CharIDDatabase.textMapHash2Text(weaponItem["flat"]["weaponStats"][1]["appendPropId"],
                                                        language="ja"),
                "value": weaponItem["flat"]["weaponStats"][1]["statValue"]
            }
        },
        "Score": {
        },
        "Artifacts": {
            "flower": artifactFlower,
            "wing": artifactWing,
            "clock": artifactClock,
            "cup": artifactCup,
            "crown": artifactCrown
        },
        "元素": CharIDDatabase.charElement(avatarData["avatarId"], language="ja")
    }
    data["Character"]["Status"].update(elementalDmg)
    data["Character"]["Talent"].update(talentInfo)
    data["Score"].update(artifactScore)

    return data


def EnkaData2ArtifactImageGeneratorData(enkaData, characterId, language):
    imgStr = ""
    for avatarInfos in enkaData["avatarInfoList"]:
        if avatarInfos["avatarId"] == characterId:
            # found the character, transform it into ArtifactImageGenerator format
            data = dataConverter(avatarData=avatarInfos, fullData=enkaData, language=language)
            imgStr = Generater.generation(data, language=language)
            break
    return imgStr
