import functools

import discord


def require_admin(func):
    @functools.wraps(func)
    async def wrapper(ctx, *args, **kwargs):
        if not ctx.message.author.guild_permissions.administrator:
            return await ctx.message.channel.send(("Insufficient Permissions: "
                                                   "You must be an administrator of the discord "
                                                   "guild **{}**.").format(ctx.message.guild.name))
        else:
            return await func(ctx, *args, **kwargs)
    return wrapper


def strip_mention(mention: str) -> str:
    if mention.startswith('<@') and mention.endswith('>'):
        mention = mention[2:-1]
        if mention.startswith('!'):
            mention = mention[1:]
    return mention


def strip_channel_mention(mention: str) -> int:
    if mention.startswith('<#') and mention.endswith('>'):
        mention = mention[2:-1]
    return int(mention)


def parse_bot_args(string_args) -> list:
    string_args = ' '.join(string_args)
    list_args = string_args.split(",")
    for i, s in enumerate(list_args):
        list_args[i] = s.lstrip().rstrip()
    return list_args


async def member_has_role(member: discord.Member,
                          role_name: str):
    if role_name.lower() in [y.name.lower() for y in member.roles]:
        return True
    return False


async def is_in_guild_roles(roles,
                            role_string: str):
    return await do_roles_match(roles, role_string, role_string)


async def is_in_list_string(list_string_to_check: list,
                            string_to_check: str):
    if string_to_check.lower() in [y.lower() for y in list_string_to_check]:
        return True
    return False


async def do_roles_match(roles,
                         role_string: str,
                         real_role_string: str) -> list:
    role = discord.utils.get(roles, name=role_string)
    real_role = discord.utils.get(roles, name=real_role_string)
    roles_match = False
    if role is None:
        roles_match = False
    elif real_role is None:
        roles_match = False
    elif role.id == real_role.id:
        roles_match = True
    return [roles_match, role, real_role]


async def embed_message(channel, title_string, name_string, value_string):
    ret_string = str("""```css\n{}```""".format(value_string))
    embed = discord.Embed(title=title_string)
    embed.add_field(name=name_string, value=ret_string)
    await channel.send(embed=embed)
