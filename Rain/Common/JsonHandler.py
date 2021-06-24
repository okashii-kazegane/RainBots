import json
import os
from pathlib import Path

import discord


class JsonHandler:
    def __init__(self, guild: discord.Guild, file_name: str):
        self.default_values: dict = dict()
        self.guild: discord.Guild = guild
        self.file_name: str = file_name
        self.flag_success: bool = False

    def setup(self) -> bool:
        if not os.path.exists(str(self.guild.name)):
            try:
                os.makedirs(str(self.guild.name))
                with open(Path(self.guild.name, self.file_name), 'w+') as json_file:
                    json.dump(self.default_values, json_file, indent=4, sort_keys=True)
            except:
                return False
        return True

    async def get(self) -> dict:
        if not self.flag_success:
            return dict()
        with open(Path(self.guild.name, self.file_name), 'r') as json_file:
            json_dict = json.load(json_file)
        return json_dict

    async def update(self, json_dict: dict) -> None:
        with open(Path(self.guild.name, self.file_name), 'w+') as json_file:
            json.dump(json_dict, json_file, indent=4, sort_keys=True)
