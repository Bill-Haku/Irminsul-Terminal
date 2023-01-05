import time

import requests
import json
import os
from botpy.ext.cog_yaml import read


config = read(os.path.join(os.path.dirname(__file__), "../config.yaml"))

url = f"https://discord.com/api/v10/applications/{config['appid']}/commands"
fileName = f"commands.json"
with open(fileName) as commandsJsonFile:
    commands = json.load(commandsJsonFile)

    headers = {
        "Authorization": f"Bot {config['token']}"
    }

    for command in commands["commands"]:
        r = requests.post(url, headers=headers, json=command)
        print(r.json())
        time.sleep(0.5)


