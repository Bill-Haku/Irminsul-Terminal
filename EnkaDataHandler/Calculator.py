import discord
import CharIDDatabase


calAvailableCharIdList = [10000046]


def calculatorHandler(charid, charData, i18n, language):
    if charid == 10000046:
        return hutaoCalculator(charData, i18n, language)
    else:
        return None


def hutaoCalculator(charData, i18n, language):
    embed = discord.Embed(title=f"{CharIDDatabase.charFullName(charData['avatarId'], language=language)}",
                          description=f"Lv. {charData['propMap']['4001']['val']}",
                          colour=0xeee657)
    fightPopMap = charData["fightPropMap"]
    skillLevelMap = charData["skillLevelMap"]
    level = charData['propMap']['4001']['val']
    constellationNum = 0
    try:
        constellationNum = len(charData["talentIdList"])
    except Exception as e:
        constellationNum = 0

    # 半血开e重击蒸发
    atk = fightPopMap["2001"]
    baseAtk = fightPopMap["1"]
    cr = fightPopMap["20"]
    cd = fightPopMap["22"]
    skillALevel = skillLevelMap["10461"]
    skillELevel = skillLevelMap["10462"]
    if constellationNum >= 3:
        skillELevel += 3
    hp = fightPopMap["2000"]
    em = fightPopMap["28"]
    pyrodb = fightPopMap["40"]
    skillAEffects = [1.36, 1.452, 1.545, 1.669, 1.761, 1.869, 2.009, 2.148, 2.287, 2.426, 2.565, 2.704, 2.843, 2.982, 3.121]
    skillEEffects = [0.0384, 0.0407, 0.043, 0.046, 0.0483, 0.0506, 0.0536, 0.566, 0.0596, 0.0626, 0.0656, 0.0685, 0.0715, 0.0745]
    witchOfFlameCount = 0
    shimenawaCount = 0
    # check if in 4 witch of flame
    for reliquary in charData["equipList"]:
        if reliquary["flat"]["itemType"] == "ITEM_RELIQUARY":
            if reliquary["flat"]["setNameTextMapHash"] == "1524173875":
                witchOfFlameCount += 1
            elif reliquary["flat"]["setNameTextMapHash"] == "4144069251":
                shimenawaCount += 1

    totalAtk = atk + hp * skillEEffects[skillELevel - 1]
    pureDmg = totalAtk * skillAEffects[skillALevel - 1]
    if shimenawaCount >= 4:
        elementalDmg = pureDmg * (1.33 + pyrodb + 0.5)
    elif witchOfFlameCount >= 4:
        elementalDmg = pureDmg * (1.33 + pyrodb + 0.075)
    else:
        elementalDmg = pureDmg * (1.33 + pyrodb)
    enemyDefPer = (int(level) + 100) / (90 + 100 + int(level) + 100)
    enemyRisPer = 0.9
    nonCritDmg = elementalDmg * enemyDefPer * enemyRisPer
    critDmg = nonCritDmg * (1 + cd)
    expectDmg = critDmg * cr + nonCritDmg * (1 - cr)
    emBonus = (2.78 * em) / (em + 1400)
    if witchOfFlameCount >= 4:
        vaporizeCritDmg = critDmg * 1.5 * (1 + emBonus + 0.15)
        vaporizeExpectDmg = expectDmg * 1.5 * (1 + emBonus + 0.15)
    else:
        vaporizeCritDmg = critDmg * 1.5 * (1 + emBonus)
        vaporizeExpectDmg = expectDmg * 1.5 * (1 + emBonus)

    embed.add_field(name=i18n["feat.cal.label.hutao.1"],
                    value=f"{round(vaporizeCritDmg)} (AVG: {round(vaporizeExpectDmg)})")
    embed.add_field(name=i18n["feat.cal.label.note"],
                    value=i18n["feat.cal.hutao.note"])
    return embed

