import discord
import CharIDDatabase


def getArtifactsDatas(charData, i18n, language):
    firstEmbed = discord.Embed(title=i18n["feat.artifacts"], description=i18n["feat.artifacts.description"] + f" {CharIDDatabase.charFullName(charData['avatarId'], language=language)}", color=0xeee657)
    embeds = [firstEmbed]
    for equip in charData["equipList"]:
        # check if equip is an artifact
        if equip["flat"]["itemType"] == "ITEM_RELIQUARY":
            embed = discord.Embed(title=CharIDDatabase.textMapHash2Text(equip["flat"]["setNameTextMapHash"], language=language),
                                  colour=0xeee657)
            # embed.add_field(name=CharIDDatabase.textMapHash2Text(equip["flat"]["nameTextMapHash"], language=language),
            #                 value=CharIDDatabase.textMapHash2Text(equip["flat"]["setNameTextMapHash"], language))
            embed.add_field(name=CharIDDatabase.textMapHash2Text(equip["flat"]["reliquaryMainstat"]["mainPropId"], language),
                            value=equip["flat"]["reliquaryMainstat"]["statValue"])
            embed.set_image(url=f"https://enka.network/ui/{equip['flat']['icon']}.png")
            for substats in equip["flat"]["reliquarySubstats"]:
                embed.add_field(name=CharIDDatabase.textMapHash2Text(substats["appendPropId"], language),
                                value=substats["statValue"], inline=False)
            embeds.append(embed)
    return embeds


def getStatsBoardDatas(charData, i18n, language):
    embed = discord.Embed(title=f"{CharIDDatabase.charFullName(charData['avatarId'], language=language)}",
                          description=f"Lv. {charData['propMap']['4001']['val']}",
                          colour=0xeee657)
    fightPopMap = charData["fightPropMap"]

    # HP
    embed.add_field(name=i18n["feat.label.hp"],
                    value=f"{round(fightPopMap['2000'], 2)} ({round(fightPopMap['1'])})")
    # ATK
    embed.add_field(name=i18n["feat.label.atk"],
                    value=f"{round(fightPopMap['2001'], 2)} ({round(fightPopMap['4'])})")
    # DEF
    embed.add_field(name=i18n["feat.label.def"],
                    value=f"{round(fightPopMap['2002'], 2)} ({round(fightPopMap['7'])})")
    # ER
    embed.add_field(name=i18n["feat.label.er"],
                    value=f"{round(fightPopMap['23'] * 100, 2)}%")
    # EM
    embed.add_field(name=i18n["feat.label.em"],
                    value=f"{round(fightPopMap['28'], 2)}")
    # Crit Rate
    embed.add_field(name=i18n["feat.label.cr"],
                    value=f"{round(fightPopMap['20'] * 100, 2)}%")
    # Crit DMG
    embed.add_field(name=i18n["feat.label.cd"],
                    value=f"{round(fightPopMap['22'] * 100, 2)}%")

    return embed
