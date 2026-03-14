import discord
from functions import direct_msg

async def ban(message):
    member = message.guild.get_member(message.author.id)
    if member is None:
        try:
            member = await message.guild.fetch_member(message.author.id)
        except discord.NotFound:
            print(f"Could not fetch member {message.author.name}.")

    try:
        try:
            await member.ban(reason=f"Sending banned text")
        except discord.Forbidden:
            print(f"Insufficient permissions to ban {message.author.name}.")
        await direct_msg(
            f"Your account has been banned because your message contains banned text",
            message,
        )
    except (discord.Forbidden, discord.HTTPException):
        print(f"Couldn't DM {message.author.name}")

async def kick(message):
    member = message.guild.get_member(message.author.id)
    if member is None:
        try:
            member = await message.guild.fetch_member(message.author.id)
        except discord.NotFound:
            print(f"Could not fetch member {message.author.name}.")

    try:
        try:
            await member.kick(reason=f"Sending banned text")
        except (discord.Forbidden, discord.HTTPException):
            print(f"Insufficient permissions to kick {message.author.name}")
        await direct_msg(
            f"Your account has been kicked because your message contains banned text",
            message
        )
    except (discord.Forbidden, discord.HTTPException):
        print(f"Couldn't DM {message.author.name}")