import discord
import logging
from discord.ui import Modal, TextInput
from discord import *
from IrminsulTerminal import i18n_en, i18n_ja, i18n_zh, config


_log = logging.getLogger('discord')
logHandler = logging.FileHandler(filename='irminsul.log', encoding='utf-8', mode='w')
_log.addHandler(logHandler)


class VoiceChannelCreator(Modal):
    def __init__(self, i18n, botName) -> None:
        super().__init__(title=i18n["sys.label.createVC"])
        self.i18n = i18n
        textInput = discord.ui.TextInput(label=i18n["sys.label.createVC.text"])
        bitRateInput = discord.ui.TextInput(label=i18n["sys.label.createVC.bitRate"], default="64000", placeholder="8000~96000/384000")
        self.add_item(textInput)
        self.add_item(bitRateInput)
        self.botName = botName

    async def on_submit(self, interaction: discord.Interaction, /) -> None:
        i18n = self.i18n
        name = self.children[0].value
        bitRateStr = self.children[1].value
        try:
            bitRate = int(bitRateStr)
        except Exception as e:
            msg = i18n["feat.createvc.fail.bitRate"]
            _log.warning(msg)
            await interaction.response.send_message(msg)
            return
        botName = self.botName
        ctx = interaction
        if config["createChannelWithPrefix"]:
            name = f"[{botName}]{name}"
        _log.info(f"Create Voice Channel {name}...")
        try:
            channel = await ctx.guild.create_voice_channel(name=name, bitrate=bitRate, category=interaction.channel.category)
            res = True
            msg = f"\"{channel.name}\" {i18n['feat.createvc.success']}\n{i18n['feat.createvc.tips']}"
        except Forbidden as forbidden:
            _log.error(f"Create voice channel fail because of Forbidden")
            res = False
            msg = i18n["feat.createvc.fail"] + "Forbidden: No permission"
        except HTTPException:
            _log.error(f"Create voice channel fail because of HTTPException")
            res = False
            msg = i18n["feat.createvc.fail"] + "HTTP Error"
        except TypeError:
            _log.error(f"Create voice channel fail because of TypeError")
            res = False
            msg = i18n["feat.createvc.fail"] + "Type Error"
        _log.info(msg)
        await interaction.response.send_message(msg, ephemeral=True)


class VoiceChannelCreatorModalView(discord.ui.View):
    def __init__(self, botName) -> None:
        super(VoiceChannelCreatorModalView, self).__init__(timeout=None)
        self.botName = botName

    @discord.ui.button(label=i18n_en["sys.label.createVC.button"], style=discord.ButtonStyle.gray,
                       custom_id="VCCreatorView:Button_en")
    async def open_modal(self, interaction: discord.Interaction, button: discord.Button):
        modal = VoiceChannelCreator(i18n=i18n_en, botName=self.botName)
        await interaction.response.send_modal(modal)

    @discord.ui.button(label=i18n_ja["sys.label.createVC.button"], style=discord.ButtonStyle.green,
                       custom_id="VCCreatorView:Button_ja")
    async def open_modal2(self, interaction: discord.Interaction, button: discord.Button):
        modal = VoiceChannelCreator(i18n=i18n_ja, botName=self.botName)
        await interaction.response.send_modal(modal)

    @discord.ui.button(label=i18n_zh["sys.label.createVC.button"], style=discord.ButtonStyle.red,
                       custom_id="VCCreatorView:Button_zh")
    async def open_modal3(self, interaction: discord.Interaction, button: discord.Button):
        modal = VoiceChannelCreator(i18n=i18n_zh, botName=self.botName)
        await interaction.response.send_modal(modal)
