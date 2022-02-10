import json
import os
from pathlib import Path

import discord


class JsonHandler:
    def __init__(self, caller_loc: str, guild: discord.Guild, file_name: str):
        self.default_values: dict = dict()
        self.guild: discord.Guild = guild
        self.file_name: str = file_name
        self.flag_success: bool = False
        self.caller_location: str = caller_loc

    def setup(self) -> bool:
        if not os.path.exists(self.caller_location + str(self.guild.name)):
            try:
                os.makedirs(self.caller_location + str(self.guild.name))
                with open(Path(self.caller_location, self.guild.name, self.file_name), 'w+') as json_file:
                    json.dump(self.default_values, json_file, indent=4, sort_keys=True)
            except:
                return False
        return True

    async def get(self) -> dict:
        if not self.flag_success:
            return dict()
        try:
            with open(Path(self.caller_location, self.guild.name, self.file_name), 'r') as json_file:
                json_dict = json.load(json_file)
        except:
            return False
        return json_dict

    async def update(self, json_dict: dict) -> None:
        with open(Path(self.caller_location, self.guild.name, self.file_name), 'w+') as json_file:
            json.dump(json_dict, json_file, indent=4, sort_keys=True)
