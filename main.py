# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import discord
from discord.ui import Button, View
from discord.ext import commands
import asyncio
from config import TOKEN  # use any file to store personal token

HEAD_FILLER = "\n|" + "=" * 25 + "|"
FILLER = "\n+" + "-" * 25 + "+"
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=commands.when_mentioned_or('?'), help_command=None, intents=intents)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Unknown command.")


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")


@bot.command()
async def hello(ctx: commands.Context):
    await ctx.send("Hey!")


# view contents and properties of sent message
@bot.command()
async def view_params(ctx: commands.Context, *args):
    if ctx.message.author.guild_permissions.administrator:
        await ctx.send(f"Message:\n{str(ctx.message)}{FILLER}")
        await ctx.send(f"Message components:\n{str(ctx.message.components)}{FILLER}")
        await ctx.send(f"Arguments:\n{str(args)}{FILLER}")
        await ctx.send(f"Author:\n{str(ctx.message.author)}{FILLER}")
        await ctx.send(f"Author Permissions:\n{str(ctx.message.author.guild_permissions)}{FILLER}")
        await ctx.send(f"Admin?:\n{str(ctx.message.author.guild_permissions.administrator)}{FILLER}")


# view basic statistics of name given in [*args] if user of such name is present in server
@bot.command()
async def stats(ctx: commands.Context, *args):
    person_arg = args[0] if len(args) == 1 else ""
    if not ctx.message.author.guild_permissions.administrator:
        await ctx.send("Must be administrator to use this command")
    else:
        if person_arg == "":
            await ctx.send(f"Invalid Arguments: {args}")
        else:
            found_person = find_person(ctx.guild, person_arg)
            if found_person is None:
                await ctx.send(f"User [{person_arg}] not found")
            else:
                await ctx.send(f"SERVER STATISTICS FOR [{person_arg}]:{HEAD_FILLER}")
                await ctx.send(f"Roles: {role_names(found_person.roles)}{FILLER}")
                await ctx.send(f"Highest Role: {str(found_person.top_role.name.replace('@', ''))}{FILLER}")


@bot.command()
@commands.has_permissions(manage_roles=True)
async def giverole(ctx: commands.Context, member: discord.Member, role: discord.Role):
    await member.add_roles(role)
    await ctx.send(f"{member.name} is now a {role.name}")


@bot.command()
@commands.has_permissions(manage_roles=True)
async def removerole(ctx: commands.Context, member: discord.Member, role: discord.Role):
    await member.remove_roles(role)
    await ctx.send(f"{member.name} is no longer a {role.name}")


@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx: commands.Context, member: discord.Member, reason: str):
    await member.kick(reason=reason)
    await ctx.send(f"Kicked [{member.name}] for {reason}")


@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx: commands.Context, member: discord.Member, reason: str):
    await member.ban(reason=reason)
    await ctx.send(f"Banned [{member.name}] for {reason}")


def find_role(ctx, name):
    for role in ctx.guild.roles:
        if role.name == name:
            return role.id
    return ""


def role_names(roles):
    retval = ""
    for role in roles:
        retval += str(role.name.replace("@", "")) + ", "
    return retval[:-2]


def find_person(server, person_name):
    for member in server.members:
        if member.name == person_name:
            return member
    return None


bot.run(TOKEN)  # run the bot with the token
