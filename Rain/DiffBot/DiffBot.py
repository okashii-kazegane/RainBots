import sys
import os

sys.path.append(os.getcwd())

import discord

import Rain.Common.Utils
from Rain.Common.AbstractBot import AbstractBot
from Rain.Common.Configs import Configs
from Rain.DiffBot.DiffChannel import DiffChannel


class DiffBot(AbstractBot):

    def __init__(self):
        super().__init__()
        AbstractBot.discordBot.command_prefix = Configs.diffbotPrefix
        diffbot_info = \
            ("Hello, I am **DiffBot**. I am a bot built to help moderate your server.\n"
             "For more info, visit __diffbot.rain-ffxiv.com__\n"
             "If you have any issues, email __oka@rain-ffxiv.com__\n\n"
             "__**Administrator commands:**__\n"
             " - **diff.info** - that's this command!\n"
             " - **diff.set *#channel-mention*** - Bot will log edits and deletions in the specified channel.\n\n")
        AbstractBot._information = [diffbot_info, AbstractBot._information]
        print(self._information)


@AbstractBot.discordBot.command()
@Rain.Common.Utils.require_admin
async def set(ctx, channel_mention):
    diffchannel_object: DiffChannel = DiffChannel(ctx.message.guild)
    found_channel = AbstractBot.discordBot.get_channel(Rain.Common.Utils.strip_channel_mention(channel_mention))
    if found_channel is not None:
        await diffchannel_object.set_log_channel_id(found_channel.id)
        await ctx.message.channel.send("Deleted message log channel is set to **#{}**".format(found_channel.name))
    else:
        await ctx.message.channel.send("That is an invalid channel.")


@AbstractBot.discordBot.event
async def on_message_edit(before: discord.Message, after: discord.Message):
    log_channel_object: DiffChannel = DiffChannel(before.guild)
    log_channel_id = await log_channel_object.get_log_channel_id()
    log_channel = AbstractBot.discordBot.get_channel(int(log_channel_id))
    if log_channel is not None:
        if before.channel.id == log_channel.id:
            return
        if before.content != after.content:
            title_str = "{} has edited a message in the {} channel ".format(before.author,
                                                                            before.channel)
            name_str = before.content
            value_str = after.content
            try:
                await Rain.Common.Utils.embed_message(log_channel, title_str, name_str, value_str)
            except:
                await log_channel.send("__**{} has edited a message in the {} channel**__".format(before.author,
                                                                                                  before.channel))
                await log_channel.send("*{}*".format(before.content))
                await log_channel.send("**{}**".format(after.content))


@AbstractBot.discordBot.event
async def on_raw_message_edit(payload):
    log_channel_object: DiffChannel = DiffChannel(AbstractBot.discordBot.get_channel(payload.channel_id).guild)
    log_channel_id = await log_channel_object.get_log_channel_id()
    log_channel = AbstractBot.discordBot.get_channel(int(log_channel_id))
    if log_channel is not None:
        if payload.channel_id == log_channel.id:
            return
        if payload.cached_message is None or                                                                       \
           not payload.cached_message.content or                                                                   \
           not payload.cached_message.content.strip():
            await log_channel.send(("**An uncached message was edited in the "
                                    "channel <#{}>**").format(payload.channel_id,
                                                              payload.channel_id))
        else:
            pass


@AbstractBot.discordBot.event
async def on_raw_message_delete(payload):
    log_channel_object: DiffChannel = DiffChannel(AbstractBot.discordBot.get_channel(payload.channel_id).guild)
    log_channel_id = await log_channel_object.get_log_channel_id()
    log_channel = AbstractBot.discordBot.get_channel(int(log_channel_id))
    if log_channel is not None:
        if payload.channel_id == log_channel.id:
            return
        if payload.cached_message is not None and                                                                  \
           payload.cached_message.content and                                                                      \
           payload.cached_message.content.strip():
            title_str = "{} has deleted a message in the {} channel ".format(payload.cached_message.author,
                                                                             payload.cached_message.channel)
            value_str = payload.cached_message.content
            name_str = "Cached message:"
            try:
                await Rain.Common.Utils.embed_message(log_channel, title_str, name_str, value_str)
            except:
                await log_channel.send(("__**{} has deleted a message in the {} "
                                        "channel**__").format(payload.cached_message.author,
                                                              payload.cached_message.channel))
                await log_channel.send("**{}**".format(payload.cached_message.content))
        else:
            await log_channel.send(("**An uncached message was deleted in the "
                                    "channel <#{}>**").format(payload.channel_id,
                                                              payload.channel_id))


if __name__ == "__main__":
    mToken = ''
    dToken = ''
    if len(sys.argv) >= 2:
        dToken = sys.argv[1]
    Configs.initialize(mToken, dToken)
    diffbot = DiffBot()
    diffbot.run(Configs.diffbotToken, reconnect=True)
