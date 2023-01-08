# User Manual of Irminsul Terminal Discord Bot

This is the user manual for all the common users of this discord bot. Here you can know what does each command means
and how to use them.

## Before you first use it

What you need to do first is to bind your Discord account with your UID of Genshin Impact. So that the bot can know 
who you are in the game.

Use it like this:

```
/bind [UID]
```

> You don't need to enter `[]` when entering UID. These square brackets means the content in it is various upon your
> self. Same in the below.

UID is an integer number between 100000000 and 999999999. Discord will check it automatically.

Next, as we support 3 different languages, you need to set your language, and the bot will remember it and answer your 
commands in your language.

All the supported languages are:
- English
- Japanese
- Simplified Chinese

> For English Users, you are lucky that you can skip this step because the default language is English.

Use it like this:

```
/setlanguage [Language]
```

For the `Language` part here, you just need to **choose from the choices** provided by Discord.

## Main features

The main features are features based on a character. Use the following command to tell the bot which character you want 
to look up about.

```
/character [Character Name]
```

> Character names in all 3 supported languages can be recognized here. Although you are suggested to use full names in 
> correct spellings, we have considered many common short names and wrong characters (in Chinese or Japanese). In addition, you should not enter a space when entering 
> the English name. Here are some examples:
> 
> - ✅: Ayaka
> - ✅: ayaka
> - ✅: kamisatoayaka
> - ❌: kamisato ayaka (no space)
> - ✅: 神里绫华
> - ✅: 绫华
> - ✅: 凌华 (wrong character)
> - ✅: 神里凌华 (wrong character)
> - ✅: 綾華
> - ✅: 神里綾華
> - ✅: 神里綾香 (wrong character)
> - ✅: あやか (kana)
> 

After that, the bot will reply you with all the function buttons available with this character. You just need to tap the
button and the bot will reply you with results.

What you need to know is that all your data is get from [Enka.Network](https://enka.network) API, and all
the data will be stored on the server after you first use it, which means your characters'
data will not be updated unless you use the `/sync` command.

## Update or Sync Your Characters' Data

If you put a new character into your character showcase in the game, or you adjusted some artifacts or weapon of
a character, you need ask the bot to sync data manually. Use the following command:

```
/sync
```

**Attention: You cannot sync too frequently. A new sync request must be raised after 2 minutes of your last sync 
request.**

## Look up Info bound with your Discord Account

You can use the following command to look up info bound with your Discord account:

```
/lookup
```

Currently, you can look up the bound UID in the database. Just tap the button.

## Any questions? Contact me!

Join my [Discord Server](https://discord.gg/XyFAGduTcM)!