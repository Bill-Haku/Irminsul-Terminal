from CharIDDatabase import locResult

dict = {
    "HP": {
        "ja": "HP",
        "zh": "生命值",
        "en": "HP"
    },
    "攻撃力": {
        "ja": "攻撃力",
        "zh": "攻击力",
        "en": "ATK"
    },
    "防御力": {
        "ja": "防御力",
        "zh": "防御力",
        "en": "DEF"
    },
    "元素熟知": {
        "ja": "元素熟知",
        "zh": "元素精通",
        "en": "EM"
    },
    "会心率": {
        "ja": "会心率",
        "zh": "暴击率",
        "en": "CRIT Rate"
    },
    "会心ダメージ": {
        "ja": "会心ダメージ",
        "zh": "暴击伤害",
        "en": "CRIT DMG"
    },
    "元素チャージ効率": {
        "ja": "元素チャージ効率",
        "zh": "元素充能效率",
        "en": "ER"
    },
    "攻撃パーセンテージ": {
        "ja": "攻撃パーセンテージ",
        "zh": "攻击力%",
        "en": "ATK%"
    },
    "防御パーセンテージ": {
        "ja": "防御パーセンテージ",
        "zh": "防御力%",
        "en": "DEF%"
    },
    "HPパーセンテージ": {
        "ja": "HPパーセンテージ",
        "zh": "生命值%",
        "en": "HP%"
    },
    "水元素ダメージ": {
        "ja": "水元素ダメージ",
        "zh": "水元素伤害加成",
        "en": "Hydro DMG"
    },
    "物理ダメージ": {
        "ja": "物理ダメージ",
        "zh": "物理伤害加成",
        "en": "Physical DMG"
    },
    "風元素ダメージ": {
        "ja": "風元素ダメージ",
        "zh": "风元素伤害加成",
        "en": "Anemo DMG"
    },
    "岩元素ダメージ": {
        "ja": "岩元素ダメージ",
        "zh": "岩元素伤害加成",
        "en": "Geo DMG"
    },
    "火元素ダメージ": {
        "ja": "火元素ダメージ",
        "zh": "火元素伤害加成",
        "en": "Pyro DMG"
    },
    "与える治癒効果": {
        "ja": "与える治癒効果",
        "zh": "治疗加成",
        "en": "Healing Bonus"
    },
    "雷元素ダメージ": {
        "ja": "雷元素ダメージ",
        "zh": "雷元素伤害加成",
        "en": "Electro DMG"
    },
    "氷元素ダメージ": {
        "ja": "氷元素ダメージ",
        "zh": "冰元素伤害加成",
        "en": "Cryo DMG"
    },
    "草元素ダメージ": {
        "ja": "草元素ダメージ",
        "zh": "草元素伤害加成",
        "en": "Dendro DMG"
    },
    "攻撃%": {
        "ja": "攻撃%",
        "zh": "攻击力%",
        "en": "ATK%"
    },
    "防御%": {
        "ja": "防御%",
        "zh": "防御力%",
        "en": "DEF%"
    },
    "HP%": {
        "ja": "HP%",
        "zh": "生命值%",
        "en": "HP%"
    },
    "元チャ効率": {
        "ja": "元チャ効率",
        "zh": "元素充能",
        "en": "ER"
    },
    "換算": {
        "ja": "換算",
        "zh": "转换",
        "en": " Conversion"
    }
}


def findInLocResult(word):
    for key in locResult["ja"]:
        if locResult["ja"][key] == word:
            return key
    return None


def translator(word, language):
    if word in dict:
        return dict[word][language]
    else:
        key = findInLocResult(word)
        if language == "zh":
            language = "zh-CN"
        if key is not None:
            return locResult[language][key]
        return word