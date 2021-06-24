class AbstractBaseAPIException(Exception):
    error_message = "API Exception:\n"


class BotPrefixError(AbstractBaseAPIException):
    error_message = AbstractBaseAPIException.error_message + ("Derived class must set a new bot prefix: "
                                                              "discordBot.command_prefix")


class AbstractBotAsMain(AbstractBaseAPIException):
    error_message = AbstractBaseAPIException.error_message + ("AbstractBot.py cannot be run as a main program. "
                                                              "Please run one of the concrete bots.")
