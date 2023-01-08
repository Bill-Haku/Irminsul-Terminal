# Project Irminsul Terminal

![GitHub](https://img.shields.io/github/license/Bill-Haku/Irminsul-Terminal)
![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/Bill-Haku/Irminsul-Terminal)

![English OK](https://img.shields.io/badge/English-✅-green) 
![Japanese OK](https://img.shields.io/badge/日本語-✅-green) 
![Chinese OK](https://img.shields.io/badge/简体中文-✅-green)
## Brief Introduction

This is a `python` project for a Discord bot. You can deploy it on your own
server or just use the bot running on my own server. Users can use it 
to get their characters' stat info, artifacts info and calculate the damage 
of some skills.

More functions will be added in the future.

This software is a part of Project Irminsul Terminal. Project Irminsul Terminal 
is a series of open-source software made by me, which is aiming at provided helpful 
tools for Genshin Impact players. Other software in this project 
includes [Genshin Pizza Helper](http://ophelper.top), an all-Apple-platforms App.
See more in the [App Store](https://apps.apple.com/app/id1635319193).

## Functions

> For further details, see `./docs`. Or you can read our user manuals:
> 
> - [English Version](http://ophelper.top/irminsul_terminal/user_manual_en)
> - [Japanese Version](http://ophelper.top/irminsul_terminal/user_manual_ja)
> - [Simplified Chinese Version](http://ophelper.top/irminsul_terminal/user_manual_zh)

- `/bind`: Bind your Discord Account ID with your Genshin UID.
- `/setlanguage`: Set the language the robot reply you when the user call a command.
- `/character [character name]`: Robot replies the user with all the available functions:
  - Character general stats: HP, ATK, Crit rate... datas
  - Artifacts info: detail info of each artifact on the character
  - Calculator: calculate the damage of some skills of this character
- `/lookup`: Look up the datas of your Discord account stored in the database
- `/sync`: Sync data of your characters in the game from [Enka.Network](https://enka.network)

Also, server administrators can use it to allow members in your server to create voice channels by themselves.
Administrations can create a readonly channel and use `/createvc` to init it. Other members can use the bot here.

## How to use this bot?

You have 3 ways to use this bot.

### Join My Server or My Friend たお's Server or any Other Server

Click [here](https://discord.gg/XyFAGduTcM) to join my server (JA/EN/ZH available).

Click [here](https://discord.gg/hutaotaotao) to join たお's server(JA mostly).

### Invite the bot running on my own server to your own server

> **Attention: I DO NOT ensure any stability or security on my server.**

Just click this [link](https://discord.com/api/oauth2/authorize?client_id=964545612831932507&permissions=8&scope=bot) to invite it!

### Deploy it on your own server

> It is recommended for you to deploy it on your own server if you can.

See in below: [How to deploy and make contributions](##Deploy and Make Contributions).

## Deploy and Make Contributions

### Finish basic configuration

First, you need to create a Discord App on Discord. You can find many tutorials on the web.

Then, a database is necessary for this bot to run. I am using MySQL here, and you'd better also use it and deploy MySQL on your server first.
And create a database called `Irminsul` (or anything else you like).

```sql
CREATE DATABASE Irminsul;
```

Now you can configure the bot. Here I provided a default `config_sample.yaml` for you.
You can finish configurations based on it.

- Rename the file to `config.yaml`
- Enter your `token` and `appid`
- Enter the connection parameters to your MySQL database. Pay attention to the database name here.
- Other settings if you want to change them.

### Install requirements

```shell
pip install -r requirements.txt
```

### Create Tables in the Databse

You can simply run the provided `./database/create.sql` in your database server.

### Upload Commands to Discord

This step allows your users to use commands just by enter `/` in the textbox and Discord App will show 
the description of each related command.

```shell
cd init
python registerCommands.py
```

### Start it!

```shell
python main.py
```

### Make Contributions

I really appreciate it if you are willing to make contributions. Any Issue is welcomed.
Also, you can make new features or fix bugs by creating PR.

## License

This Project is released under [MIT License](./LICENSE).