import secrets

import discord

from Rain.Common.Configs import Configs
from Rain.Common.JsonHandler import JsonHandler


class Roles(JsonHandler):
    def __init__(self, guild: discord.Guild):
        super().__init__("Rain\\Monsoon\\", guild, Configs.jsonConfigFileName)
        self.default_values[Configs.roleAdminIndex] = secrets.token_urlsafe(24)
        self.default_values[Configs.roleNamesIndex] = []
        self.default_values[Configs.roleAssignableIndex] = []
        self.flag_success = self.setup()

    async def get_admin(self):
        json_dict = await self.get()
        return json_dict[Configs.roleAdminIndex]

    async def set_admin(self, admin: str):
        json_dict: dict = await self.get()
        json_dict[Configs.roleAdminIndex] = admin
        await self.update(json_dict)

    async def get_names(self):
        json_dict: dict = await self.get()
        return json_dict[Configs.roleNamesIndex]

    async def set_names(self, names):
        json_dict: dict = await self.get()
        json_dict[Configs.roleNamesIndex] = names
        await self.update(json_dict)

    async def get_assignable(self):
        json_dict = await self.get()
        return json_dict[Configs.roleAssignableIndex]

    async def set_assignable(self, assignable):
        json_dict: dict = await self.get()
        json_dict[Configs.roleAssignableIndex] = assignable
        await self.update(json_dict)
