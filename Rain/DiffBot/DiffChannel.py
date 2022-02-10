import secrets

from Rain.Common.Configs import Configs
from Rain.Common.JsonHandler import JsonHandler


class DiffChannel(JsonHandler):
    def __init__(self, guild) -> None:
        super().__init__("Rain\\DiffBot\\", guild, Configs.diffConfigFileName)
        self.default_values[Configs.diffchannelIndex] = secrets.token_urlsafe(24)
        self.flag_success = self.setup()

    async def get_log_channel_id(self) -> str:
        json_dict: dict = await self.get()
        return json_dict[Configs.diffchannelIndex]

    async def set_log_channel_id(self, channel_id):
        json_dict: dict = await self.get()
        json_dict[Configs.diffchannelIndex] = channel_id
        await self.update(json_dict)
