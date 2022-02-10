import sys
from typing import List

import Rain.Common.Utils
from Rain.Common.AbstractBot import AbstractBot
from Rain.Common.Configs import Configs
from Rain.Monsoon.Greeting import Greeting
from Rain.Monsoon.Roles import Roles


class Monsoon(AbstractBot):

    def __init__(self):
        super().__init__()
        AbstractBot.discordBot.command_prefix = Configs.monsoonPrefix
        monsooninfo = \
            ("Hello, I am **Monsoon**.  I am a bot built to help moderate your server. \n"
             "For more info, you can visit my website at __monsoon.rain-ffxiv.com__\n"
             "If you have any issues, email __oka@rain-ffxiv.com__\n\n"
             "__**General commands:**__\n"
             " - **m.info** - that's this command!\n"
             "- **m.me** OR **m.print_roles** - Prints all the roles that you can assign to or revoke from other "
             "users.\n "
             " - **m.me *role name*** - Assign yourself the specified role.\n"
             "- **m.request *role name*** - Notifies people with permission to assign the requested role that you "
             "wish to be assigned to that role.\n\n "
             "__**Privileged commands:**__\n"
             "- **m.role *@user, role name*** - assigns the role to the mentioned user. Be sure to include the comma, "
             "and make sure you are using an @mention for the user's name (requires the subject to have access to the "
             "channel you are currently in).\n "
             "- **m.role *@user, role name, revoke*** - revokes the role from the mentioned user. Be sure to include "
             "the comma, and make sure you are using an @mention for the user's name.\n\n "
             "__**Administrator commands:**__\n"
             "- **m.edit_role *first role name, second role name*** - gives members with the first role permission to "
             "assign or revoke the second role to/from other members. Don't forget the comma!\n "
             "- **m.edit_role *first role name, second role name, revoke*** - members with the first role LOSE their "
             "permission to assign or revoke the second role to/from other members. Don't forget the comma!\n "
             "- **m.edit_greeting *\"The greeting you want to send new members\"*** - when a member joins the server, "
             "they will get a private message from the bot according to the message you set with this command.\n "
             "- **m.prev_greeting** - get a preview of the greeting that you have set. If no greeting is set, "
             "you will not get a message.\n\n "
             )
        extramonsooninfo = (Configs.paragraphSeparator +
                            "**Roles that can be requested:**"
                            "\n\t\t**Rain**"
                            "\n\t\t**Guest Starring**"
                            "\n\t\t**VRC**"
                            "\n\t\t**D&D**"
                            "\n\t\t**DJ** (should be granted only temporarily)\n\n"
                            "**Roles that can be self-assigned:**\n\t\t"
                            "**FFXIV**\n\t\t"
                            "**PartyTime**\n\t\t"
                            "**VRC**\n\t\t"
                            "**Ark**\n\t\t"
                            "**Minecraft**\n\t\t"
                            "**Crafting/Gathering Requests**\n\t\t"
                            "**Behemoth Server**\n\t\t"
                            "**Primal Data Center**\n\t\t"
                            "**Crystal Data Center**\n\t\t"
                            "**Aether Data Center**\n\t\t"
                            "**Stardew**\n\t\t"
                            "**Vikings**\n\n")

        AbstractBot._information = [monsooninfo, extramonsooninfo, AbstractBot._information]
        print(self._information)


@AbstractBot.discordBot.event
async def on_member_join(member) -> None:
    greeting_object = Greeting(member.guild.name)
    greeting_string = await greeting_object.get()
    if greeting_string and greeting_string.strip():
        await member.send(greeting_string)


@AbstractBot.discordBot.command()
async def print_roles(ctx):
    commander = ctx.message.author
    roles_object: Roles = Roles(ctx.message.guild)
    roles: dict = await roles_object.get()
    if not roles:
        # if roles is an empty dict object
        await ctx.message.channel.send("Error: No roles were fetched. Message @Okashii#0001 or oka@rain-ffxiv.com")
        return
    name_list: List[str] = roles[Configs.roleNamesIndex]
    for i, role_name in enumerate(name_list):
        if not await Rain.Common.Utils.member_has_role(commander, role_name):
            # if there's no match, skip to the next item in name_list
            continue
        count = len(roles[Configs.roleAssignableIndex][i])
        # count is now the number of roles that the current role has permission to assign
        if count > 0:
            await ctx.message.channel.send(("{}: you can assign yourself and others {} role(s) "
                                            "because you are a member of the elevated role"
                                            "\n**__{}__**:"
                                            "\n\t\t**{}**").format(commander.mention,
                                                                   count,
                                                                   role_name.strip('@'),
                                                                   " \n\t\t".join(
                                                                       roles[Configs.roleAssignableIndex][i]
                                                                   )
                                                                   )
                                           )


@AbstractBot.discordBot.command()
@Rain.Common.Utils.require_admin
async def edit_greeting(ctx, *string_args) -> None:
    greeting_object = Greeting(ctx.message.guild.name)
    greeting_string = ' '.join(string_args)
    # noinspection PyBroadException
    try:
        greeting_object.update(greeting_string)
    except:
        await ctx.message.channel.send(("There was a problem updating the greeting for this server. Message "
                                        "@Okashii#0001 or oka@rain-ffxiv.com"))
        return
    await ctx.message.channel.send("Greeting updated.")


@AbstractBot.discordBot.command()
@Rain.Common.Utils.require_admin
async def prev_greeting(ctx):
    greeting_object = Greeting(ctx.message.guild.name)
    greeting_string = greeting_object.get()
    if not greeting_string:
        await ctx.message.channel.send("There was a problem with fetching this server's greeting.")
        return
    if greeting_string and greeting_string.strip():
        await ctx.message.author.send(greeting_string)
        await ctx.message.channel.send("Greeting preview sent. Check your private messages.")


@AbstractBot.discordBot.command()
@Rain.Common.Utils.require_admin
async def edit_role(ctx, *string_args):
    list_args: List[str] = Rain.Common.Utils.parse_bot_args(string_args)
    elevated_rolename_arg = list_args[0]
    rolename_arg = list_args[1]
    revoke = False
    if len(list_args) == 3:
        revoke = True
    [flag_is_elevated_role_in_guild_roles,
     elevated_role_arg,
     _] = await Rain.Common.Utils.is_in_guild_roles(ctx.message.guild.roles,
                                                    elevated_rolename_arg)
    if not flag_is_elevated_role_in_guild_roles:
        await ctx.message.channel.send(("Specified elevated role **__{}__** does not "
                                        "exist!").format(elevated_rolename_arg.strip('@')))
        return
    elevated_rolename_arg = elevated_role_arg.name
    [flag_is_role_in_guild_roles,
     role_arg,
     _] = await Rain.Common.Utils.is_in_guild_roles(ctx.message.guild.roles,
                                                    rolename_arg)
    if not flag_is_role_in_guild_roles:
        await ctx.message.channel.send(("Specified role **__{}__** does not "
                                        "exist!").format(rolename_arg.strip('@')))
        return
    rolename_arg = role_arg.name
    try:
        role_object = Roles(ctx.message.guild)
        roles = await role_object.get()
        if not roles:
            await ctx.message.channel.send("There was a problem fetching roles. "
                                           "Message @Okashii#0001")
            return
        roles[Configs.roleAdminIndex] = str(ctx.message.author.id)
        name_list: List[str] = roles[Configs.roleNamesIndex]
        if elevated_rolename_arg not in name_list:
            roles[Configs.roleNamesIndex].append(elevated_rolename_arg)
            roles[Configs.roleAssignableIndex].append([])
        i = name_list.index(elevated_rolename_arg)
        in_assignable_roles = rolename_arg in roles[Configs.roleAssignableIndex][i]
        if revoke and in_assignable_roles:
            j = roles[Configs.roleAssignableIndex][i].index(rolename_arg)
            roles[Configs.roleAssignableIndex][i].pop(j)
            await ctx.message.channel.send(("Elevated role **__{}__** editing privileges for role **__{}__** have "
                                            "been revoked.").format(elevated_rolename_arg.strip('@'),
                                                                    rolename_arg.strip('@')))
        elif not revoke and not in_assignable_roles:
            roles[Configs.roleAssignableIndex][i].append(rolename_arg)
            await ctx.message.channel.send(
                ("Elevated role **__{}__** members have been granted editing "
                 "privileges for role **__{}__**.").format(elevated_rolename_arg.strip('@'),
                                                           rolename_arg.strip('@'))
            )
        if not len(roles[Configs.roleAssignableIndex][i]) > 0:
            roles[Configs.roleAssignableIndex].pop(i)
            roles[Configs.roleNamesIndex].pop(i)
            await ctx.message.channel.send(("Elevated role **__{}__** has been "
                                            "de-elevated.").format(elevated_rolename_arg.strip('@')))
        await role_object.update(roles)
    except:
        await ctx.message.channel.send(("Failure to verify. Ask oka@rain-ffxiv.com to troubleshoot. "
                                        "Or message @Okashii#0001"))
        raise


@AbstractBot.discordBot.command()
async def me(ctx, *string_args):
    if not string_args:
        await print_roles(ctx)
        return
    new_string_args = (ctx.message.author.mention, ',', *string_args)
    await role(ctx, *new_string_args)


@AbstractBot.discordBot.command()
async def role(ctx, *string_args):
    success_flag = False
    list_args: List[str] = Rain.Common.Utils.parse_bot_args(string_args)
    user_mention_arg = list_args[0]
    username_arg = Rain.Common.Utils.strip_mention(user_mention_arg)
    rolename_arg = list_args[1]
    revoke = False
    if len(list_args) == 3:
        revoke = True
    [flag_is_in_guild_roles, role_arg, _] = await Rain.Common.Utils.is_in_guild_roles(ctx.message.guild.roles,
                                                                                      rolename_arg)
    if not flag_is_in_guild_roles:
        await ctx.message.channel.send(("Specified role **__{}__** does not "
                                        "exist!").format(rolename_arg.strip('@')))
        return

    user_arg = ctx.message.guild.get_member(int(username_arg))

    if user_arg is None:
        await ctx.message.channel.send(("Please contact oka@rain-ffxiv.com. "
                                        "Finding members by mention is not working "
                                        "for this member."))
        return
    try:
        role_object = Roles(ctx.message.guild)
        roles = await role_object.get()
        if not roles:
            await ctx.message.channel.send(("There was a problem fetching roles for this server."
                                            " Contact oka@rain-ffxiv.com or message @Okashii#0001."))
            return
        name_list: List[str] = await role_object.get_names()
        for i, elevatedRoleName in enumerate(name_list):
            if not await Rain.Common.Utils.member_has_role(ctx.message.author, elevatedRoleName):
                continue
            if not await Rain.Common.Utils.is_in_list_string(roles[Configs.roleAssignableIndex][i], rolename_arg):
                continue
            if await Rain.Common.Utils.member_has_role(user_arg,
                                                       elevatedRoleName) and \
                    user_arg != ctx.message.author:
                await ctx.message.channel.send(("{}: you may not change role assignments for other elevated "
                                                "users.").format(ctx.message.author.mention))
                success_flag = False
                break
            success_flag = True
        if success_flag:
            if not revoke:
                await user_arg.add_roles(role_arg)
                await ctx.message.channel.send(("{} has assigned the **__{}__** role to "
                                                "{}").format(ctx.message.author.mention,
                                                             rolename_arg.strip('@'),
                                                             user_arg.mention))
            else:
                await user_arg.remove_roles(role_arg)
                await ctx.message.channel.send(("{} has revoked the **__{}__** role from "
                                                "{}").format(ctx.message.author.mention,
                                                             rolename_arg.strip('@'),
                                                             user_arg.mention))
        else:
            await ctx.message.channel.send(("{}: your command failed. If you have permission to change the "
                                            "assignment, then double check the format of your "
                                            "request.").format(ctx.message.author.mention))
    except:
        await ctx.message.channel.send(("Failure to verify. Ask oka@rain-ffxiv.com to troubleshoot"
                                        " or message @Okashii#0001."))
        raise


@AbstractBot.discordBot.command()
async def request(ctx, *string_args):
    success_flag = False
    list_args = Rain.Common.Utils.parse_bot_args(string_args)
    rolename_arg = list_args[0]
    if Configs.debugMode:
        print(rolename_arg)
        print("-")
    [is_in_guild_roles, role_arg, _] = await Rain.Common.Utils.is_in_guild_roles(ctx.message.guild.roles,
                                                                                 rolename_arg)
    if not is_in_guild_roles:
        await ctx.message.channel.send(("Specified role {} does not exist!".format(rolename_arg)))
        return
    try:
        role_object = Roles(ctx.message.guild)
        roles = await role_object.get()
        if not roles:
            await ctx.message.channel.send("There was a problem.")
            return
        if Configs.debugMode:
            print(role_arg)
            print("-")
        for i, listOfRoles in enumerate(roles[Configs.roleAssignableIndex]):
            if Configs.debugMode:
                print(i)
                print(listOfRoles)
                print("-")
            is_role_in_list = await Rain.Common.Utils.is_in_list_string(listOfRoles, rolename_arg)
            if is_role_in_list:
                [is_role_in_guild_roles, elevated_role, _] = \
                    await Rain.Common.Utils.is_in_guild_roles(ctx.message.guild.roles,
                                                              roles[Configs.roleNamesIndex][i])
                if Configs.debugMode:
                    print(ctx.message.guild.roles)
                    print(roles[Configs.roleNamesIndex][i])
                    print(is_role_in_guild_roles)
                    print(elevated_role)
                    print("-")
                author_role_match = await Rain.Common.Utils.member_has_role(ctx.message.author,
                                                                            roles[Configs.roleNamesIndex][i])
                if author_role_match:
                    await ctx.message.channel.send(("{}, you can assign this role to yourself. Type "
                                                    "**m.me {}**").format(ctx.message.author.mention,
                                                                          role_arg.name))
                else:
                    await ctx.message.channel.send(("{}, please assign {} the {} "
                                                    "role.").format(elevated_role.mention,
                                                                    ctx.message.author.mention,
                                                                    role_arg.name))
                success_flag = True
                break
        if not success_flag:
            admin_user = \
                ctx.message.guild.get_member(int(Rain.Common.Utils.strip_mention(roles[Configs.roleAdminIndex])))
            await ctx.message.channel.send("{}, please assign {} the {} role.".format(admin_user.mention,
                                                                                      ctx.message.author.mention,
                                                                                      role_arg.name))
    except:
        await ctx.message.channel.send("Failure to verify. Ask oka@rain-ffxiv.com to troubleshoot.")
        raise


if __name__ == "__main__":
    mToken = ''
    dToken = 'Error'
    if len(sys.argv) >= 2:
        mToken = sys.argv[1]
    Configs.initialize(mToken, dToken)
    monsoon = Monsoon()
    monsoon.run(Configs.monsoonToken, reconnect=True)
