import discord
import logging
from discord.ui import Modal, TextInput
from discord import *
from IrminsulTerminal import i18n_en, i18n_ja, i18n_zh, config, IrminsulTerminal


_log = logging.getLogger('discord')
logHandler = logging.FileHandler(filename='irminsul.log', encoding='utf-8', mode='w')
_log.addHandler(logHandler)


class CharacterInfoManager(Modal):
    def __init__(self, i18n, botName) -> None:
        super().__init__(title=i18n["sys.label.charinfo.button"])
        self.i18n = i18n
        textInput = discord.ui.TextInput(label=i18n["sys.label.charname"])
        self.add_item(textInput)
        self.botName = botName

    async def on_submit(self, interaction: discord.Interaction, /) -> None:
        i18n = self.i18n
        charName = self.children[0].value
        _log.info(f"{interaction.user.name}#{interaction.user.id}: Look up character: {charName}...")
        terminal = IrminsulTerminal(language="ja")
        resTitle, resView = terminal.lookUpChar(userID=interaction.user.id, charName=charName, isPrivate=True)
        await interaction.response.send_message(resTitle, view=resView, ephemeral=True)


class CharInfoModalView(discord.ui.View):
    def __init__(self, botName) -> None:
        super(CharInfoModalView, self).__init__(timeout=None)
        self.botName = botName

    @discord.ui.button(label=i18n_ja["sys.label.charinfo.button"], style=discord.ButtonStyle.gray,
                       custom_id="CharInfo:Button")
    async def open_modal(self, interaction: discord.Interaction, button: discord.Button):
        modal = CharacterInfoManager(i18n=i18n_ja, botName=self.botName)
        await interaction.response.send_modal(modal)
