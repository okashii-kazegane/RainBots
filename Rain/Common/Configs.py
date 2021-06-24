import os

import discord


class Configs:
    intents = discord.Intents.default()
    intents.typing = False
    intents.presences = False
    intents.members = True
    monsoonToken: str = ''
    diffbotToken: str = ''
    debugMode: bool = False
    jsonConfigFileName: str = 'config.json'
    diffConfigFileName: str = 'diffconfig.json'
    greetingFileName: str = 'greeting.txt'
    max_messages: int = 20000000
    defaultPrefix = "ABSTRACTBOTDEFAULTPREFIX"
    monsoonPrefix = "m."
    diffbotPrefix = "diff."
    paragraphSeparator = "\n\n\t\t\t\t----------------------------\n\n"
    roleNamesIndex = 'names'
    roleAssignableIndex = 'assignable'
    roleAdminIndex = 'admin'
    diffchannelIndex = 'log_channel_id'

    @classmethod
    def initialize(cls, mtoken, dtoken):
        if mtoken:
            cls.monsoonToken = mtoken
        else:
            cls.monsoonToken = os.environ['MONSOON_TOKEN']
        if dtoken:
            cls.diffbotToken = dtoken
        else:
            cls.diffbotToken = os.environ['DIFFBOT_TOKEN']
