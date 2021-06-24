from abc import ABC, abstractmethod

import discord
from discord.ext import commands

import Rain.Common.Utils
import Rain.Exceptions
from Rain.Common.Configs import Configs


class AbstractBot(ABC):

    discordBot: discord.ext.commands.bot = commands.Bot(command_prefix=Configs.defaultPrefix,
                                                        max_messages=Configs.max_messages,
                                                        intents=Configs.intents)
    _information = (Configs.paragraphSeparator +
                    "Discord server bot created by __@Okashii#0001__ for the Rain Discord server "
                    "(__discord.rain-ffxiv.com__).\n"
                    "For assistance, please email __Oka@rain-ffxiv.com__\n"
                    "For more information about this bot, please see http://bots.rain-ffxiv.com\n\n")

    @abstractmethod
    def __init__(self):
        self._information = ("\nDiscord server bot created by @Okashii#0001 for the Rain Discord server "
                             "(discord.rain-ffxiv.com).\n"
                             "For assistance, please email Oka@rain-ffxiv.com\n"
                             "For more information about this bot, please see http://bots.rain-ffxiv.com")

    @classmethod
    def information(cls):
        return cls._information

    def run(self, *args, **kwargs):
        if self.discordBot.command_prefix != Configs.defaultPrefix:
            self.discordBot.run(*args, **kwargs)
        else:
            raise Rain.Exceptions.BotPrefixError(Rain.Exceptions.BotPrefixError.error_message)


@AbstractBot.discordBot.command()
async def info(ctx):
    for i in AbstractBot.information():
        await ctx.send(i)


@AbstractBot.discordBot.event
async def on_message(message: discord.Message) -> None:
    # we do not want the bot to reply to itself
    if message.author == AbstractBot.discordBot.user:
        return
    await AbstractBot.discordBot.process_commands(message)


@AbstractBot.discordBot.event
async def on_ready() -> None:
    print('Logged in as')
    print(AbstractBot.discordBot.user.name)
    print(AbstractBot.discordBot.user.id)
    print('------')
    game = discord.CustomActivity(name="bots.rain-ffxiv.com")
    await AbstractBot.discordBot.change_presence(activity=game)


if __name__ == "__main__":
    raise Rain.Exceptions.AbstractBotAsMain(Rain.Exceptions.AbstractBotAsMain.error_message)
