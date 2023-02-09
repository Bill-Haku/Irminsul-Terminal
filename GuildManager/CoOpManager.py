import discord
import logging
from discord.ui import Modal, TextInput
from discord import *
from IrminsulTerminal import i18n_en, i18n_ja, i18n_zh, config, IrminsulTerminal
from GuildManager.CharacterInfoButton import CharacterInfoManager


_log = logging.getLogger('discord')
logHandler = logging.FileHandler(filename='irminsul.log', encoding='utf-8', mode='w')
_log.addHandler(logHandler)


class CoOpManager(Modal):
    def __init__(self, i18n, role: discord.Role) -> None:
        super().__init__(title=i18n["sys.label.coop.title"])
        self.i18n = i18n
        self.role = role
        threadTitleInput = discord.ui.TextInput(label=i18n["sys.coop.input.label.1"])
        typeInput = discord.ui.TextInput(label=i18n["sys.coop.input.label.2"], default=role.name)
        requirementInput = discord.ui.TextInput(label=i18n["sys.coop.input.label.3"])
        contentInput = discord.ui.TextInput(label=i18n["sys.coop.input.label.4"])
        worldRankInput = discord.ui.TextInput(label=i18n["sys.coop.input.label.5"], default="8")
        # noteInput = discord.ui.TextInput(label=i18n["sys.coop.input.label.6"], required=False)
        self.add_item(threadTitleInput)
        self.add_item(typeInput)
        self.add_item(requirementInput)
        self.add_item(contentInput)
        self.add_item(worldRankInput)
        # self.add_item(noteInput)

    async def on_submit(self, interaction: discord.Interaction, /) -> None:
        await interaction.response.defer()
        i18n = self.i18n
        threadTitle = self.children[0].value
        type = self.children[1].value
        requirement = self.children[2].value
        contents = self.children[3].value
        worldRank = self.children[4].value
        # note = self.children[5].value
        _log.info(f"{interaction.user.name}#{interaction.user.id}: Sent a Co-Op raise")
        terminal = IrminsulTerminal(language="ja")

        coopPublicChannelId = config["test"]["coopChannelId"]
        if interaction.guild.id == config["test"]["id"]:
            coopPublicChannelId = config["test"]["coopChannelId"]
        elif interaction.guild.id == config["tao"]["id"]:
            coopPublicChannelId = config["tao"]["coopChannelId"]

        coopPublicChannel = discord.utils.get(interaction.guild.channels, id=coopPublicChannelId)

        embed = discord.Embed(title=f"{interaction.user.name}{i18n['sys.coop.embed.title']}")
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)
        embed.add_field(name=i18n["sys.coop.input.label.2"], value=type)
        embed.add_field(name=i18n["sys.coop.input.label.3"], value=requirement)
        embed.add_field(name=i18n["sys.coop.input.label.4"], value=contents)
        embed.add_field(name=i18n["sys.coop.input.label.5"], value=worldRank)
        # if note is not None and note != "":
        #     embed.add_field(name=i18n["sys.coop.input.label.6"], value=note)
        publicThread = await coopPublicChannel.create_thread(name=threadTitle, type=discord.ChannelType.public_thread)
        _log.info(f"create thread {publicThread.name} success")
        publicThreadButton = AfterLinkModalView(url=publicThread.jump_url)
        publicMessage = await coopPublicChannel.send(content=f"{self.role.mention}", embed=embed, view=publicThreadButton)
        privateButtonsView = PrivateManagementButtons(thread=publicThread, interactionStarted=interaction, publicMessage=publicMessage)
        managementMessage = await interaction.followup.send(embed=embed, view=privateButtonsView)
        privateButtonsView.updateMessage(managementMessage)
        _log.info(f"send message {publicMessage.id} success")
        await publicThread.send(embed=embed)
        _log.info(f"{interaction.user.name} raise co-op post all done")


class AfterLinkModalView(discord.ui.View):
    def __init__(self, url, label=i18n_ja["sys.coop.afterlink.title"]) -> None:
        super(AfterLinkModalView, self).__init__(timeout=None)
        button1 = discord.ui.Button(label=label, url=url)
        self.add_item(button1)


class PrivateManagementButtons(discord.ui.View):
    def __init__(self,
                 thread: discord.Thread,
                 interactionStarted: discord.Interaction,
                 publicMessage: discord.Message,
                 message: discord.Message = None,) -> None:
        super(PrivateManagementButtons, self).__init__(timeout=None)
        self.thread = thread
        self.interactionStarted = interactionStarted
        self.message = message
        button1 = discord.ui.Button(label=i18n_ja["sys.coop.afterlink.title"], url=thread.jump_url)
        self.add_item(button1)
        self.publicMessage = publicMessage

    @discord.ui.button(label=i18n_ja["sys.label.coop.button.stop"], style=discord.ButtonStyle.red)
    async def stopThread(self, interaction: discord.Interaction, button: discord.Button):
        _log.info(f"{interaction.user.name} stop {self.interactionStarted.user.name}'s thread: {self.thread.name}")
        if interaction.user.id == self.interactionStarted.user.id:
            await self.thread.edit(locked=True, archived=True)
            await interaction.response.send_message(content=i18n_ja["sys.label.coop.button.stop.done"], ephemeral=True)
            await self.publicMessage.edit(content=i18n_ja["sys.label.raise.end"])
            await self.message.delete()
            _log.info(f"{interaction.user.name} end thread {self.thread.name} done")

    def updateMessage(self, message: discord.Message):
        self.message = message


selectOption1 = discord.SelectOption(label=i18n_ja["sys.label.copy"], value=config["tao.roles"][5])
selectOption2 = discord.SelectOption(label=i18n_ja["sys.label.materials"], value=config["tao.roles"][6])
selectOption3 = discord.SelectOption(label=i18n_ja["sys.label.boss"], value=config["tao.roles"][7])
selectOption4 = discord.SelectOption(label=i18n_ja["sys.label.exploration"], value=config["tao.roles"][9])
selectOption5 = discord.SelectOption(label=i18n_ja["sys.label.others"], value=config["tao.roles"][8])
selectOptions = [selectOption1, selectOption2, selectOption3, selectOption4, selectOption5]


class CoOpManagerModalView(discord.ui.View):
    def __init__(self) -> None:
        super(CoOpManagerModalView, self).__init__(timeout=None)

    @discord.ui.select(cls=discord.ui.Select,
                       options=selectOptions,
                       placeholder=i18n_ja["sys.coop.select.placeholder"],
                       custom_id="CoOp:Select",
                       min_values=0)
    async def raiseCoopFromSelectedTypes(self, interaction: discord.Interaction, select: discord.ui.Select):
        _log.info(f"{interaction.user.name} selected {select.values[0]} to try raise co-op")
        if interaction.user.guild.id == config["tao"]["id"]:
            role = interaction.guild.get_role(int(select.values[0]))
            if role is None:
                _log.info(f"role is none")
            else:
                _log.info(f"mention {role.name} when raising co-op")
            modal = CoOpManager(i18n=i18n_ja, role=role)
            await interaction.response.send_modal(modal)
