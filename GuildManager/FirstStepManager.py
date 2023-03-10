import discord
import logging
from discord.ui import Modal, TextInput
from discord import *
from IrminsulTerminal import i18n_en, i18n_ja, i18n_zh, config, IrminsulTerminal
from GuildManager.CharacterInfoButton import CharacterInfoManager


_log = logging.getLogger('discord')
logHandler = logging.FileHandler(filename='irminsul.log', encoding='utf-8', mode='w')
_log.addHandler(logHandler)


class BindUIDManager(Modal):
    def __init__(self, i18n, botName) -> None:
        super().__init__(title=i18n["sys.label.binduid.button"])
        self.i18n = i18n
        textInput = discord.ui.TextInput(label=i18n["sys.label.uid"])
        self.add_item(textInput)
        self.botName = botName

    async def on_submit(self, interaction: discord.Interaction, /) -> None:
        i18n = self.i18n
        uid = self.children[0].value
        _log.info(f"{interaction.user.name}#{interaction.user.id}: Bind UID {uid}...")
        terminal = IrminsulTerminal(language="ja")
        result = terminal.bindUID(user=interaction.user, uid=uid)
        if result == i18n["msg.bindUidSuccess"]:
            resLang = terminal.setLanguage(user=interaction.user, language="ja")
            if resLang == i18n["msg.setLanguageSuccess"]:
                result += f"\n{i18n['msg.tips.afterbinduid']}"
        await interaction.response.send_message(result, ephemeral=True)


class FirstStepManagerModalView(discord.ui.View):
    def __init__(self, botName) -> None:
        super(FirstStepManagerModalView, self).__init__(timeout=None)
        self.botName = botName

    @discord.ui.button(label=i18n_ja["sys.label.binduid.button"], style=discord.ButtonStyle.gray,
                       custom_id="BindUID:Button")
    async def open_bind_modal(self, interaction: discord.Interaction, button: discord.Button):
        modal = BindUIDManager(i18n=i18n_ja, botName=self.botName)
        await interaction.response.send_modal(modal)

    @discord.ui.button(label=i18n_ja["sys.label.charinfo.button"], style=discord.ButtonStyle.gray,
                       custom_id="CharInfo:Button")
    async def open_charinfo_modal(self, interaction: discord.Interaction, button: discord.Button):
        modal = CharacterInfoManager(i18n=i18n_ja, botName=self.botName)
        await interaction.response.send_modal(modal)

    @discord.ui.button(label=i18n_ja["sys.label.sync.button"], style=discord.ButtonStyle.gray,
                       custom_id="SyncInfo:Button")
    async def sync_enka_data(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.defer()
        terminal = IrminsulTerminal(language="ja")
        res = terminal.updateEnkaData(userID=interaction.user.id)
        await interaction.followup.send(res, ephemeral=True)

    @discord.ui.button(label=i18n_ja["sys.label.deluid.button"], style=discord.ButtonStyle.red,
                       custom_id="DelUID:Button")
    async def del_uid(self, interaction: discord.Interaction, button: discord.Button):
        terminal = IrminsulTerminal(language="ja")
        res = terminal.delUserRecord(userID=interaction.user.id)
        await interaction.response.send_message(res, ephemeral=True)
