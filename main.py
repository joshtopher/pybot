import discord
from discord.ui import Button, View
from discord.ext import commands
import asyncio
from config import TOKEN  # use any file to store personal token

HEAD_FILLER = "\n|" + "=" * 25 + "|"
FILLER = "\n+" + "-" * 25 + "+"
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=commands.when_mentioned_or('?'),
                   help_command=commands.DefaultHelpCommand(), intents=intents)
message_id = -1
verified_role = None


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Unknown command.")
    else:
        await ctx.send("Something went wrong. Please refer to '?help' to check if the command is being used properly.")


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")


# view contents and properties of sent message
@bot.command()
@commands.has_permissions(administrator=True)
async def view_params(ctx: commands.Context, *args):
    await ctx.send(f"Message:\n{str(ctx.message)}{FILLER}")
    await ctx.send(f"Message components:\n{str(ctx.message.components)}{FILLER}")
    await ctx.send(f"Arguments:\n{str(args)}{FILLER}")
    await ctx.send(f"Author:\n{str(ctx.message.author)}{FILLER}")
    await ctx.send(f"Author Permissions:\n{str(ctx.message.author.guild_permissions)}{FILLER}")
    await ctx.send(f"Admin?:\n{str(ctx.message.author.guild_permissions.administrator)}{FILLER}")


# view basic statistics of member
@bot.command()
async def stats(ctx: commands.Context, member: discord.Member):
    await ctx.send(f"SERVER STATISTICS FOR [{member.name}]:{HEAD_FILLER}")
    await ctx.send(f"Roles: {role_names(member.roles)}{FILLER}")
    await ctx.send(f"Highest Role: {str(member.top_role.name.replace('@', ''))}{FILLER}")


@bot.command(aliases=['giverole'])
@commands.has_permissions(manage_roles=True)
async def give_role(ctx: commands.Context, member: discord.Member, role: discord.Role):
    await member.add_roles(role)
    await ctx.send(f"{member.name} is now a {role.name}")


@bot.command(aliases=['removerole'])
@commands.has_permissions(manage_roles=True)
async def remove_role(ctx: commands.Context, member: discord.Member, role: discord.Role):
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


# Sets the verify message
@bot.command(aliases=['setverify'])
@commands.has_permissions(administrator=True)
async def set_verify_channel(ctx: commands.Context):
    verification_message = await ctx.channel.send("Please react to this message to verify your membership.")
    global message_id
    message_id = verification_message.id


# Sets the role given when user is verified
@bot.command(aliases=['setverifyrole'])
@commands.has_permissions(administrator=True)
async def set_verified_role(ctx: commands.Context, role: discord.Role):
    global verified_role
    verified_role = role
    await ctx.send(f"Verified role set to {role.name}")


#when the 'verify message' is reacted to, this function gives the 'verify role' to the user who reacted
@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id != message_id:
        return
    await payload.member.add_roles(verified_role)


def role_names(roles):
    retval = ""
    for role in roles:
        retval += str(role.name.replace("@", "")) + ", "
    return retval[:-2]


bot.run(TOKEN)  # run the bot with the token
