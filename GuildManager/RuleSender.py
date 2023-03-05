import discord
import logging
from discord.ui import Modal, TextInput
from discord import *
from IrminsulTerminal import i18n_en, i18n_ja, i18n_zh, config, IrminsulTerminal
from GuildManager.CharacterInfoButton import CharacterInfoManager

_log = logging.getLogger('discord')
logHandler = logging.FileHandler(filename='irminsul.log', encoding='utf-8', mode='w')
_log.addHandler(logHandler)

selectOption1 = discord.SelectOption(label="English", value="en")
selectOption2 = discord.SelectOption(label="日本語", value="ja")
selectOption3 = discord.SelectOption(label="简体中文", value="zh-cn")
selectOption4 = discord.SelectOption(label="繁體中文", value="zh-tw")
selectOption5 = discord.SelectOption(label="한국어", value="kr")
selectOptions = [selectOption1, selectOption2, selectOption3, selectOption4, selectOption5]


rules_ja = """<:UI_EmotionIcon65min:985536230529851402> しっかり1番下まで行ってねー！<:hutao:985536236305399858> 

 🔰ルール <:HuTaoHeart2:1075823539493544107> 

> **１.人を不快にさせる発言投稿をしない**
 「暴言や、卑猥な発言、画像を送るなどといった行動」
 
> *** ２.個人情報を投稿しない***
 「フレンドIDは個人情報に含まれません。LINEのQRコードなどを指します
 
> *** ３.R18などの有害コンテンツを投稿しない***
「卑猥な画像や、グロテスクな画像などといったもの」

> *** ４.スパムや自己宣伝、他者宣伝行為を行わない***
【宣伝は決められた場所ですること】

> ***５.常識的なマナーを守る***

> *** ６.メンションを多用しない***
「あまり多くの人を一気にメンションするのはやめてねー！」

> ***７.管理人からの指示には必ず従うこと！***

> ***８.この鯖内で起きた個人間でのトラブルや、問題等につきましては一切責任を負いません。***

> ***９.他のコンテンツクリエイターの悪口を言わない***

> ***１０.宗教、政治に関する話題をださないこと***

> ***１１.決められたチャンネルで発言すること***
「原神の話なら原神雑談、日常の話なら雑談でやってね！」

⚠️ 注意事項 ⚠️

---ルールに違反した場合---
1回違反したら「注意」
2回違反したら「厳重注意」
のロールが付きます！

3回違反したら「BAN」
↑BANする前に管理人達で話し合って決めます！

※違反してしまって、ロールがついた方へ↓

「月に一回」管理人同士で違反した人達に関して違反の取り消しについて話し合います。
反省が見られる場合はそこで違反ロールの取り消しを行います。


---他の鯖やTwitterなどで問題等を起こしている方に関して---
管理人同士で話し合って、BANするか話し合います
"""


rules_en = """<:UI_EmotionIcon65min:985536230529851402> Make sure you get to the bottom one! <:hutao:985536236305399858>

 🔰Rules <:HuTaoHeart2:1075823539493544107>

> **1. Do not post remarks that offend people**.
 Behavior such as abusive language, obscene remarks, sending pictures, etc."

> ***2.Do not post personal information***.
 (Friend IDs are not included in personal information, and refer to QR codes on LINE, etc.)

> ***3.Do not post R18 or other harmful content***.
Such as obscene or grotesque images.

> ***4.Do not spam, self-promote, or promote others***.
Do not post advertisements in designated areas.

> ***5. Observe common sense manners***.

> *** 6. Don't use too many mentions***.
Don't mention too many people at once!

> *** 7. Always follow instructions from the administrator! ***

> ***8. We are not responsible for any problems or issues that occur between individuals within this saba. ***

> ***9. Do not speak ill of other content creators***.

> ***10.Do not discuss topics related to religion or politics***.

> ***11.Speak only on the channel that you have been assigned***.
If you want to talk about Genshin Impact, do it in Genshin Impact Chat Channel, if you want to talk about daily life, do it in Chat channel!

⚠️ Notes ⚠️

---If you violate any of the rules---.
One violation will result in a "Caution"
Two violations will result in a "Caution" and a "Severe Caution" role!
will be rolled!

Ban" for 3 violations
↑upBefore banning, the administrators will discuss and decide!

To those who have violated the rules and have been given a role

Once a month, the administrators will discuss with each other about the revocation of the rolls for those who have violated the rules.
If there is a sign of remorse, the roll will be revoked.


---If you are causing problems on other servers or on Twitter, etc...
The administrators will discuss and decide whether to ban the offender or not.
"""


rules_zhtw = """🔰頻道規則<:HuTaoHeart2:1075823539493544107> 

> **１.請勿發表令人不快的言論**
 「具有辱罵性、淫穢言論、發送圖片等等的行為」
 
> *** ２.請勿發布個人的信息***
 「原神的uid並不包含在此項。此處指的是例如像Line的QR(ID)、Facebook等個人信息」
 
> *** ３.請勿發布R18相關等有害內容***
「不雅、令人感到不適的圖像」

> *** ４.請勿發送垃圾信息、自我宣傳或給他人宣傳***
【如果要做此類行為，我們擁有專屬的頻道】

> ***５.請遵守常識的禮儀***
 
> *** ６.請不要一次提及太多人***
「例如@everyone或@很多的成員等等！」

> ***７.請務必遵守管理員的指示！***

> ***８.對於本伺服器發生個人之間的任何糾紛或問題，我們概不負責。***

> ***９.不可惡意批評其他創作者***

> ***１０.不可談論宗教、政治***

> ***１１.在指定的頻道發言***
「如果是談論原神的請在 <#1076462824471134268> 、如果是在談論日常生活，請在 <#1074000217944367215> ！」

2023/3/6 修正

⚠️ 注意事項 ⚠️

---如果你違反了以上規則---.
一次違反將會導致你收到一個 "警告"
兩次違反將會導致你收到一個 "嚴重警告" 的身份組！

三次違反將會導致你被封禁！
↑被封禁之前，管理員將會討論並決定！

對於違反規則並被給予身份組的人：

每個月，管理員將會討論並決定是否撤銷違反規則的身份組。
如果你有悔改的跡象，身份組將會被撤銷。


---如果你在其他服務器或者Twitter等地方造成了惡劣影響...
管理員將會討論並決定是否封禁違規者！
"""

rules_zhcn = """🔰频道规则<:HuTaoHeart2:1075823539493544107> 

> **１.请勿发表令人不快的言论**
 「具有辱骂性、淫秽言论、淫秽图片等等的行为」

> *** ２.请勿发布个人隐私信息***
 「原神的uid并不包含在此中。此初指的是例如像Line的二维码（ID）、Facebook、QQ、微信等个人信息」

> *** ３.请勿发布R18相关等有害内容***
「不雅、令人感到不适的图像」

> *** ４.请勿发送垃圾信息、自我宣传或者给他人宣传***
【如果要做此类行为，我们拥有专属的频道】

> ***５.请遵守常识的礼仪***

> *** ６.请不要一次@太多人***
「例如@everyone或@很多的成员等等！」

> ***７.请务必遵守管理员的要求！***

> ***８.对于本服务器发生个人之间的任何纠纷或问题，我们概不负责。***

> ***９.不可恶意批评其他创作者***

> ***１０.不可谈论宗教、政治***

> ***１１.在指定的频道发言***
「如果是谈论原神的请在 <#1076462824471134268> 、如果是在谈论日常生活，请在 <#1074000217944367215> ！」

2023/3/6 修订

⚠️ 注意事项 ⚠️

---如果你违反了以上规则---.
一次违反将会导致你收到一个 "警告"
两次违反将会导致你收到一个 "严重警告" 的身份组！

三次违反将会导致你被封禁！
↑被封禁之前，管理员将会讨论并决定！

对于违反规则并被给予身份组的人：

每个月，管理员将会讨论并决定是否撤销违反规则的身份组。
如果你有悔改的迹象，身份组将会被撤销。


---如果你在其他服务器或者Twitter等地方造成了恶劣影响...
管理员将会讨论并决定是否封禁违规者！
"""


rules_kr = """💎규칙에 기재된 항목이 아니더라도 서버 및 유저에게 피해를 주는 행위는 처벌 받을 수 있습니다.

> 1. **모든 채팅채널 및 음성채널에서는 정치, 패드립, 섹드립, 타인 비하,등 의 발언은 일절 금지합니다.**
> 
> 2. **서버 내 편가르기 행위 및 분쟁 및 분쟁유도, 선동행위는 일절 금지합니다.**
> 
> 3. **모든 채팅방에서 판매를 목적으로 하는 글, 유출과 관련된 사진 및 채팅은 일절 금지합니다.**
> 
> 4. **상호 간의 과도한 멘션은 금지해주세요. 스태프에게 문의할 사항이 있다면 해당 국가 스태프에게 개인디엠으로 부탁드립니다!**
> 
> 5. **청소년 유해 매체를 금지합니다**
>       사진이나 대화에 음란성의 의도가 있다고 판단되는 경우
>       의도적인 경우 방 테러로 간주
> 
> 6. **타 크리에이터를 향한 비방 및 까내리는 행위를 일절 금지합니다.**
> 
> 7. **각 채널의 주제에 알맞는 채팅을 부탁드립니다.**


**⚠️주의사항⚠️**

**--- 규칙을 위반한 경우 ---**
1회 위반하면 '주의'
2회 위반하면 엄중주의
역할이 부여됩니다!

3번 위반하면 'BAN'
↑진행 전에 관리자들과 상의해서 결정합니다!

**※ 규칙을 위반하여 역할이 부여된 분들의 경우, ↓**

> '한 달에 한 번' 스태프 간의 회의를 통해서 규칙을 위반한 유저분들의 역할 취소를 결정합니다.
> 유저에게서 개선의 여지가 보이는 경우에 해당 위반 역할을 취소합니다.


**※ 타플랫폼에서 물의를 일으킨 유저의 경우, ↓**

> 스태프간의 가벼운 회의를 통해 해당 유저의 제재 여부를 결정합니다.
> 

모든 처벌의 사유와 내역은 관리자전용 경고처리 채널에 남습니다."""


class TaoRuleSenderModalView(discord.ui.View):
    def __init__(self) -> None:
        super(TaoRuleSenderModalView, self).__init__(timeout=None)

    @discord.ui.select(cls=discord.ui.Select,
                       options=selectOptions,
                       placeholder="Choose your language here",
                       custom_id="Tao_Send_Rule:Select")
    async def assignLangRoles(self, interaction: discord.Interaction, select: discord.ui.Select):
        _log.info(f"{interaction.user.name} selected {select.values[0]}")

        if interaction.user.guild.id == config["tao"]["id"]:
            selectItem = select.values[0]
            try:
                if selectItem == "en":
                    await interaction.response.send_message(rules_en, ephemeral=True)
                elif selectItem == "ja":
                    await interaction.response.send_message(rules_ja, ephemeral=True)
                elif selectItem == "zh-cn":
                    await interaction.response.send_message(rules_zhcn, ephemeral=True)
                elif selectItem == "zh-tw":
                    await interaction.response.send_message(rules_zhtw, ephemeral=True)
                elif selectItem == "kr":
                    await interaction.response.send_message(rules_kr, ephemeral=True)
                else:
                    _log.info(f"Unknown select item {selectItem}")
            except HTTPException as e:
                _log.exception(f"send rule for {interaction.user.name} met exception")

