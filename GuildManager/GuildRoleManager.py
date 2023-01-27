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