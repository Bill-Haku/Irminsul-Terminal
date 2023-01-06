import requests
import logging


_log = logging.getLogger('discord')
logHandler = logging.FileHandler(filename='irminsul.log', encoding='utf-8', mode='w')
_log.addHandler(logHandler)

# en zh-Hans ja names and their common wrong spellings
ayakaNames = ["10000002", "ayaka", "kamisatoayaka", "绫华", "神里绫华", "神里凌华", "凌华", "綾華", "神里綾華", "神里綾香", "綾香", "あやか"]
jeanNames = ["10000003", "jean", "琴", "ジン", "じん"]
aetherNames = ["10000005", "aether", "空", "男主", "そら"]
lisaNames = ["10000006", "lisa", "丽莎", "りさ", "リサ"]
lumineNames = ["10000007", "lumine", "荧", "莹", "萤", "蛍", "ほたる", "ホタル"]
barbaraNames = ["10000014", "barbara", "芭芭拉", "バーバラ", "ばーばら"]
kaeyaNames = ["10000015", "kaeya", "凯亚", "ガイア", "がいあ"]
dilucNames = ["10000016", "diluc", "迪卢克", "ディルック", "でぃるっく"]
razorNames = ["10000020", "razor", "雷泽", "レザー","れざー"]
amberNames = ["10000021", "amber", "安柏", "安博", "安泊", "あんばー", "アンバー"]
ventiNames = ["10000022", "venti", "温迪", "ウェンティー", "うぇんてぃー", "バルバトス", "ばるばとす"]
xianglingNames = ["10000023", "xiangling", "香菱", "シャンリン", "しゃんりん"]
beidouNames = ["10000024", "beidou", "北斗", "ホクト", "ほくと"]
xingqiuNames = ["10000025", "xingqiu", "行秋", "ユクアキ", "ゆくあき"]
xiaoNames = ["10000026", "xiao", "魈", "ショウ", "しょう"]
ningguangNames = ["10000027", "ningguang", "凝光", "ギョウコウ", "ぎょうこう"]
kleeNames = ["10000029", "klee", "可莉", "クレー", "くれー"]
zhongliNames = ["10000030", "zhongli", "钟离", "鍾離", "ショウリ", "しょうり", "モラクス", "もらくす"]
fischlNames = ["10000031", "fischl", "菲谢尔", "皇女", "小艾米", "フィッシュル", "ふぃっしゅる"]
bennettNames = ["10000032", "bennett", "班尼特", "ベネット", "べねっと"]
tartagliaNames = ["10000033", "tartaglia", "childe", "达达利亚", "公子", "タルタリヤ", "たるたりや"]
noelleNames = ["10000034", "noelle", "诺艾尔", "女仆", "ノエル", "のえる"]
qiqiNames = ["10000035", "qiqi", "七七", "77", "なな", "ナナ"]
chongyunNames = ["10000036", "chongyun", "重云", "重雲", "ちょううん", "チョウウン"]
ganyuNames = ["10000037", "ganyu", "甘雨", "カンウ", "かんう"]
albedoNames = ["10000038", "albedo", "阿贝多", "阿倍多", "アルベド", "あるべど"]
dionaNames = ["10000039", "diona", "迪奥娜", "ディオナ", "でぃおな"]
monaNames = ["10000041", "mona", "莫娜", "モナ", "もな"]
keqingNames = ["10000042", "keqing", "刻晴", "コクセイ", "こくせい"]
sucroseNames = ["10000043", "sucrose", "砂糖", "スクロース", "すくろーす"]
xinyanNames = ["10000044", "xinyan", "辛焱", "辛炎", "シンエン", "しんえん"]
rosariaNames = ["10000045", "rosaria", "罗莎莉亚", "罗莎莉娅", "ロサリア", "ろさりあ"]
hutaoNames = ["10000046", "hutao", "胡桃", "ふーたお", "フータオ", "くるみ"]
kazuhaNames = ["10000047", "kazuha", "kaedeharakazuha", "枫原万叶", "万叶", "万葉", "カズハ", "かずは", "楓原", "楓原万葉"]
yanfeiNames = ["10000048", "yanfei", "烟绯", "烟霏", "煙緋", "エンヒ", "えんひ"]
yoimiyaNames = ["10000049", "yoimiya", "宵宫", "霄宫", "ヨイミヤ", "よいみや"]
thomaNames = ["10000050", "thoma", "托马", "拖马", "トーマ", "とーま"]
eulaNames = ["10000051", "eula", "优菈", "尤拉", "エウルア", "えうるあ"]
shogunNames = ["10000052", "shogun", "raidenshogun", "shougun", "雷电将军", "雷神", "雷军", "雷電将軍", "影", "雷電", "将軍", "ライデンショウグン", "らいでんしょうぐん", "バアルゼブル", "ばあるぜぶる"]
sayuNames = ["10000053", "sayu", "早柚", "サユ", "さゆ"]
kokomiNames = ["10000054", "kokomi", "sangonomiyakokomi", "心海", "珊瑚宫心海", "珊瑚宮心海" "さんごのみやここみ", "サンゴノミヤココミ", "ここみ", "ココミ", "サンゴノミヤ", 'さんごのみや']
gorouNames = ["10000055", "gorou", "五郎", "ゴロー", "ごろー"]
kujoNames = ["10000056", "kujo", "sara", "kujosara", "九条", "九条裟罗", "九条纱罗", "九条裟羅", "くじょうさら", "クジョウサラ", "くじょう", "クジョウ", "サラ", "さら"]
ittoNames = ["10000057", "itto", "aratakiitto", "荒泷一斗", "一斗", "荒瀧一斗", "あらたきいっと", "アラタキイット", "あらたき", "アラタキ", "いっと", "イット"]
mikoNames = ["10000058", "miko", "yaemiko", "yae", "八重神子", "八重", "神子", "やえみこ", "ヤエミコ", "ミコ", "みこ", "ヤエ", "やえ"]
heizouNames = ["10000059", "heizou", "shikanoinheizou", "鹿野院平藏", "平藏", "鹿野院平蔵", "平蔵", "シカノインヘイゾウ", "しかのいんへいぞう", "シカノイン", "しかのいん", "ヘイゾウ", "へいぞう"]
yelanNames = ["10000060", "yelan", "夜兰", "夜阑", "夜蘭", "いぇらん", "イェラン", "いえらん","イエラン"]
aloyNames = ["10000062", "aloy", "埃洛伊", "アーロイ", "あーろい"]
shenheNames = ["10000063", "shenhe", "申鹤", "申鶴", "シンカク", "しんかく"]
yunjinNames = ["10000064", "yunjin", "云堇", "云瑾", "雲菫", "ウンキン", "うんきん"],
shinobuNames = ["10000065", "shinobu", "kukishinobu", "久岐忍", "忍", "くきしのぶ", "クキシノブ", "しのぶ", "シノブ", "クキ", "くき"]
ayatoNames = ["10000066", "ayato", "kamisatoayato", "神里绫人", "神里凌人", "绫人", "凌人", "綾人", "神里綾人", "かみさとあやと", "カミサトアヤト", "あやと", "アヤト"]
colleiNames = ["10000067", "collei", "柯莱", "コレイ", "これい"]
doriNames = ["10000068", "dori", "多莉", "ドリー", "どりー", "ドリ", "どり"]
tighnariNames = ["10000069", "tighnari", "提纳里", "提那里", "ティナリ", "てぃなり"]
nilouNames = ["10000070", "nilou", "妮露", "ニィロウ", "にぃろう"]
cynoNames = ["10000071", "cyno", "赛诺", "せの", "セノ"]
candaceNames = ["10000072", "candace", "坎蒂丝", "キャンディス", "きゃんでぃす"]
nahidaNames = ["10000073", "nahida", "纳西妲", "草神", "そうしん", "ソウシン", "ナヒーダ", "なひーだ", "ぶえる", "ブエル", "クラクサナビデリ", "くらくさなびでり"]
laylaNames = ["10000074", "layla", "莱依拉", "レイラ", "れいら"]
wandererNames = ["10000075", "wanderer", "balladeer", "scaramouche", "流浪者", "散兵", "伞兵", "マシュ", "ましゅ", "スカラマッシュ", "すからまっしゅ"]
faruzanNames = ["10000076", "faruzan", "珐露珊", "ファルザン", "ふぁるざん"]

locResponse = requests.get("http://ophelper.top/api/players/loc.json")
locResult = locResponse.json()

def charName2IDConverter(name):
    name = name.lower()
    if name in ayakaNames:
        return 10000002
    elif name in jeanNames:
        return 10000003
    elif name in aetherNames:
        return 10000005
    elif name in lisaNames:
        return 10000006
    elif name in lumineNames:
        return 10000007
    elif name in barbaraNames:
        return 10000014
    elif name in kaeyaNames:
        return 10000015
    elif name in dilucNames:
        return 10000016
    elif name in razorNames:
        return 10000020
    elif name in amberNames:
        return 10000021
    elif name in ventiNames:
        return 10000022
    elif name in xianglingNames:
        return 10000023
    elif name in beidouNames:
        return 10000024
    elif name in xingqiuNames:
        return 10000025
    elif name in xiaoNames:
        return 10000026
    elif name in ningguangNames:
        return 10000027
    elif name in kleeNames:
        return 10000029
    elif name in zhongliNames:
        return 10000030
    elif name in fischlNames:
        return 10000031
    elif name in bennettNames:
        return 10000032
    elif name in tartagliaNames:
        return 10000033
    elif name in noelleNames:
        return 10000034
    elif name in qiqiNames:
        return 10000035
    elif name in chongyunNames:
        return 10000036
    elif name in ganyuNames:
        return 10000037
    elif name in albedoNames:
        return 10000038
    elif name in dionaNames:
        return 10000039
    elif name in monaNames:
        return 10000041
    elif name in keqingNames:
        return 10000042
    elif name in sucroseNames:
        return 10000043
    elif name in xinyanNames:
        return 10000044
    elif name in rosariaNames:
        return 10000045
    elif name in hutaoNames:
        return 10000046
    elif name in kazuhaNames:
        return 10000047
    elif name in yanfeiNames:
        return 10000048
    elif name in yoimiyaNames:
        return 10000049
    elif name in thomaNames:
        return 10000050
    elif name in eulaNames:
        return 10000051
    elif name in shogunNames:
        return 10000052
    elif name in sayuNames:
        return 10000053
    elif name in kokomiNames:
        return 10000054
    elif name in gorouNames:
        return 10000055
    elif name in kujoNames:
        return 10000056
    elif name in ittoNames:
        return 10000057
    elif name in mikoNames:
        return 10000058
    elif name in heizouNames:
        return 10000059
    elif name in yelanNames:
        return 10000060
    elif name in aloyNames:
        return 10000062
    elif name in shenheNames:
        return 10000063
    elif name in yunjinNames:
        return 10000064
    elif name in shinobuNames:
        return 10000065
    elif name in ayatoNames:
        return 10000066
    elif name in colleiNames:
        return 10000067
    elif name in doriNames:
        return 10000068
    elif name in tighnariNames:
        return 10000069
    elif name in nilouNames:
        return 10000070
    elif name in cynoNames:
        return 10000071
    elif name in candaceNames:
        return 10000072
    elif name in nahidaNames:
        return 10000073
    elif name in laylaNames:
        return 10000074
    elif name in wandererNames:
        return 10000075
    elif name in faruzanNames:
        return 10000076
    else:
        return 0


def charFullName(charID, language):
    charResponse = requests.get("http://ophelper.top/api/players/characters.json")
    charResult = charResponse.json()
    nameTextMapHash = charResult[f"{charID}"]["NameTextMapHash"]
    locResponse = requests.get("http://ophelper.top/api/players/loc.json")
    locResult = locResponse.json()

    if language == "zh":
        language = "zh-CN"
    return locResult[f"{language}"][f"{nameTextMapHash}"]


def textMapHash2Text(nameTextMapHash, language):

    if language == "zh":
        language = "zh-CN"

    try:
        res = locResult[f"{language}"][f"{nameTextMapHash}"]
    except Exception as e:
        _log.warning(f"find text {nameTextMapHash} fail: {e}")
        res = nameTextMapHash
    return res

