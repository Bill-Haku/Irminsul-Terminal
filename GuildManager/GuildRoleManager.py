import discord
import logging
from discord.ui import Modal, TextInput
from discord import *
from IrminsulTerminal import i18n_en, i18n_ja, i18n_zh, config, IrminsulTerminal
from GuildManager.CharacterInfoButton import CharacterInfoManager


_log = logging.getLogger('discord')
logHandler = logging.FileHandler(filename='irminsul.log', encoding='utf-8', mode='w')
_log.addHandler(logHandler)


class TaoRoleLinkModalView(discord.ui.View):
    def __init__(self) -> None:
        super(TaoRoleLinkModalView, self).__init__(timeout=None)
        button1 = discord.ui.Button(label=i18n_ja["tao.link.button.1"], url=i18n_ja["tao.link.button.1.url"])
        button2 = discord.ui.Button(label=i18n_ja["tao.link.button.2"], url=i18n_ja["tao.link.button.2.url"])
        button3 = discord.ui.Button(label=i18n_ja["tao.link.button.3"], url=i18n_ja["tao.link.button.3.url"])
        button4 = discord.ui.Button(label=i18n_ja["tao.link.button.4"], url=i18n_ja["tao.link.button.4.url"])
        button5 = discord.ui.Button(label=i18n_ja["tao.link.button.5"], url=i18n_ja["tao.link.button.5.url"])
        self.add_item(button1)
        self.add_item(button2)
        self.add_item(button3)
        self.add_item(button4)
        self.add_item(button5)


class TaoFanRoleManagerModalView(discord.ui.View):
    def __init__(self) -> None:
        super(TaoFanRoleManagerModalView, self).__init__(timeout=None)

    @discord.ui.button(label="👻🍑", style=discord.ButtonStyle.green, custom_id="FanRole:Button")
    async def add_role_fan(self, interaction: discord.Interaction, button: discord.Button):
        try:
            role = discord.utils.get(interaction.guild.roles, id=config["tao.roles"][2])
            await interaction.user.add_roles(role)
            res = i18n_ja["msg.success.5"]
            _log.info(f"Add role {role.name} for {interaction.user.name} success")
        except Exception as e:
            _log.info(f"{e}")
            res = i18n_ja["msg.fail"]
        await interaction.response.send_message(res, ephemeral=True)

    @discord.ui.button(label="👻🍑🚫", style=discord.ButtonStyle.red, custom_id="DelFanRole:Button")
    async def del_role_fan(self, interaction: discord.Interaction, button: discord.Button):
        try:
            role = discord.utils.get(interaction.guild.roles, id=config["tao.roles"][2])
            await interaction.user.remove_roles(role)
            res = i18n_ja["msg.success.6"]
            _log.info(f"Remove role {role.name} for {interaction.user.name} success")
        except Exception as e:
            _log.info(f"{e}")
            res = i18n_ja["msg.fail"]
        await interaction.response.send_message(res, ephemeral=True)


class TaoSpoilerRoleManagerModalView(discord.ui.View):
    def __init__(self) -> None:
        super(TaoSpoilerRoleManagerModalView, self).__init__(timeout=None)

    @discord.ui.button(label="ON", style=discord.ButtonStyle.green, custom_id="SpoilerONRole:Button")
    async def add_role_spoiler_ok(self, interaction: discord.Interaction, button: discord.Button):
        try:
            role = discord.utils.get(interaction.guild.roles, id=config["tao.roles"][3])
            await interaction.user.add_roles(role)
            res = i18n_ja["msg.success.7"]
            _log.info(f"Add role {role.name} for {interaction.user.name} success")
        except Exception as e:
            _log.info(f"{e}")
            res = i18n_ja["msg.fail"]
        await interaction.response.send_message(res, ephemeral=True)

    @discord.ui.button(label="OFF", style=discord.ButtonStyle.red, custom_id="SpoilerOFFRole:Button")
    async def del_role_spoiler_ok(self, interaction: discord.Interaction, button: discord.Button):
        try:
            role = discord.utils.get(interaction.guild.roles, id=config["tao.roles"][3])
            await interaction.user.remove_roles(role)
            res = i18n_ja["msg.success.8"]
            _log.info(f"Remove role {role.name} for {interaction.user.name} success")
        except Exception as e:
            _log.info(f"{e}")
            res = i18n_ja["msg.fail"]
        await interaction.response.send_message(res, ephemeral=True)


class TaoRoleManagerModalView(discord.ui.View):
    def __init__(self, botName) -> None:
        super(TaoRoleManagerModalView, self).__init__(timeout=None)
        self.botName = botName

    @discord.ui.button(label=i18n_ja["tao.role.genshin.add"], style=discord.ButtonStyle.green,
                       custom_id="AddGenshinRole:Button")
    async def add_role_genshin(self, interaction: discord.Interaction, button: discord.Button):
        try:
            role = discord.utils.get(interaction.guild.roles, id=config["tao.roles"][0])
            await interaction.user.add_roles(role)
            res = i18n_ja["msg.success.1"]
            _log.info(f"Add role {role.name} for {interaction.user.name} success")
        except Exception as e:
            _log.info(f"{e}")
            res = i18n_ja["msg.fail"]
        await interaction.response.send_message(res, ephemeral=True)

    @discord.ui.button(label=i18n_ja["tao.role.genshin.del"], style=discord.ButtonStyle.red,
                       custom_id="DelGenshinRole:Button")
    async def del_role_genshin(self, interaction: discord.Interaction, button: discord.Button):
        try:
            role = discord.utils.get(interaction.guild.roles, id=config["tao.roles"][0])
            await interaction.user.remove_roles(role)
            res = i18n_ja["msg.success.2"]
            _log.info(f"Remove role {role.name} for {interaction.user.name} success")
        except Exception as e:
            _log.info(f"{e}")
            res = i18n_ja["msg.fail"]
        await interaction.response.send_message(res, ephemeral=True)

    @discord.ui.button(label=i18n_ja["tao.role.gossip.add"], style=discord.ButtonStyle.green,
                       custom_id="AddGossipRole:Button")
    async def add_role_gossip(self, interaction: discord.Interaction, button: discord.Button):
        try:
            role = discord.utils.get(interaction.guild.roles, id=config["tao.roles"][1])
            await interaction.user.add_roles(role)
            res = i18n_ja["msg.success.3"]
            _log.info(f"Add role {role.name} for {interaction.user.name} success")
        except Exception as e:
            _log.info(f"{e}")
            res = i18n_ja["msg.fail"]
        await interaction.response.send_message(res, ephemeral=True)

    @discord.ui.button(label=i18n_ja["tao.role.gossip.del"], style=discord.ButtonStyle.red,
                       custom_id="DelGossipRole:Button")
    async def del_role_gossip(self, interaction: discord.Interaction, button: discord.Button):
        try:
            role = discord.utils.get(interaction.guild.roles, id=config["tao.roles"][1])
            await interaction.user.remove_roles(role)
            res = i18n_ja["msg.success.4"]
            _log.info(f"Remove role {role.name} for {interaction.user.name} success")
        except Exception as e:
            _log.info(f"{e}")
            res = i18n_ja["msg.fail"]
        await interaction.response.send_message(res, ephemeral=True)


selectOption1 = discord.SelectOption(label="English", value="en")
selectOption2 = discord.SelectOption(label="日本語", value="ja")
selectOption3 = discord.SelectOption(label="中文", value="zh")
selectOption4 = discord.SelectOption(label="Русский", value="ru")
selectOptions = [selectOption1, selectOption2, selectOption3, selectOption4]


class HakuUserLanguageRoleManagerModalView(discord.ui.View):
    def __init__(self) -> None:
        super(HakuUserLanguageRoleManagerModalView, self).__init__(timeout=None)

    @discord.ui.select(cls=discord.ui.Select,
                       options=selectOptions,
                       placeholder="Choose your language here",
                       max_values=4,
                       custom_id="Haku_Lang_Role:Select")
    async def assignLangRoles(self, interaction: discord.Interaction, select: discord.ui.Select):
        _log.info(f"{interaction.user.name} selected {select.values[0]}")
        if interaction.user.guild.id == config["haku"]["id"]:
            hakuJaRole = interaction.guild.get_role(int(config["haku"]["roles"]["ja"]))
            hakuEnRole = interaction.guild.get_role(int(config["haku"]["roles"]["en"]))
            hakuZhRole = interaction.guild.get_role(int(config["haku"]["roles"]["zh"]))
            hakuRuRole = interaction.guild.get_role(int(config["haku"]["roles"]["ru"]))
            # remove all language roles
            try:
                await interaction.user.remove_roles(hakuJaRole, hakuRuRole, hakuZhRole, hakuEnRole)
                _log.info(f"remove all roles for {interaction.user.name} success")
            except HTTPException as e:
                _log.exception(f"remove all roles for {interaction.user.name} met exception")
            res = False
            for selectItem in select.values:
                try:
                    if selectItem == "en":
                        await interaction.user.add_roles(hakuEnRole)
                        res = True
                        _log.info(f"Added role {hakuEnRole.name} for {interaction.user.name} success")
                    elif selectItem == "ja":
                        await interaction.user.add_roles(hakuJaRole)
                        res = True
                        _log.info(f"Added role {hakuJaRole.name} for {interaction.user.name} success")
                    elif selectItem == "zh":
                        await interaction.user.add_roles(hakuZhRole)
                        res = True
                        _log.info(f"Added role {hakuZhRole.name} for {interaction.user.name} success")
                    elif selectItem == "ru":
                        await interaction.user.add_roles(hakuRuRole)
                        res = True
                        _log.info(f"Added role {hakuRuRole.name} for {interaction.user.name} success")
                    else:
                        res = False
                        _log.info(f"Unknown select item {selectItem}")
                except HTTPException as e:
                    res = False
                    _log.exception(f"add role for {interaction.user.name} met exception")

            if res:
                await interaction.response.send_message("✅", ephemeral=True)
            else:
                await interaction.response.send_message("❌", ephemeral=True)
