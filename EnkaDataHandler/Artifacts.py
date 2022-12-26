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
