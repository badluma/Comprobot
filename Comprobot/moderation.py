from datetime import timedelta
from random import choice

import discord

from .bot import client
from .data import config, moderation, output
from .functions import direct_msg


async def ban(message, item):
    member = message.guild.get_member(message.author.id)
    if member is None:
        try:
            member = await message.guild.fetch_member(message.author.id)
        except discord.NotFound:
            print(f"Could not fetch member {message.author.name}.")

    try:
        try:
            await member.ban(reason=output["moderation"]["reason"])
        except discord.Forbidden:
            print(f"Insufficient permissions to ban {message.author.name}.")
        await direct_msg(
            choice(output["moderation"]["ban"]).replace("{{TEXT}}", item),
            message,
        )
    except (discord.Forbidden, discord.HTTPException):
        print(f"Couldn't DM {message.author.name}")


async def kick(message, item):
    member = message.guild.get_member(message.author.id)
    if member is None:
        try:
            member = await message.guild.fetch_member(message.author.id)
        except discord.NotFound:
            print(f"Could not fetch member {message.author.name}.")

    try:
        try:
            await member.kick(reason=output["moderation"]["reason"])
        except (discord.Forbidden, discord.HTTPException):
            print(f"Insufficient permissions to kick {message.author.name}.")
        await direct_msg(
            choice(output["moderation"]["kick"]).replace("{{TEXT}}", item),
            message,
        )
    except (discord.Forbidden, discord.HTTPException):
        print(f"Couldn't DM {message.author.name}")


async def check_message(message):
    if message.guild is None:
        return

    if (
        message.author == client.user
        or (
            isinstance(message.author, discord.Member)
            and message.author.guild_permissions.administrator
        )
    ) and not config["debug_mode"]:
        return

    for item in moderation["delete"]:
        if item.lower() in message.content.lower():
            await message.delete()
            await direct_msg(
                choice(output["moderation"]["delete"]).replace("{{TEXT}}", item),
                message,
            )

    for item in moderation["kick"]:
        if item.lower() in message.content.lower():
            await kick(message, item)

    for item in moderation["ban"]:
        if item.lower() in message.content.lower():
            await ban(message, item)

    for item in moderation["mute"]:
        if item.lower() in message.content.lower():
            await message.delete()

            member = message.guild.get_member(message.author.id)
            if member is None:
                try:
                    member = await message.guild.fetch_member(message.author.id)
                except discord.NotFound:
                    print(f"Could not fetch member {message.author.name}.")
                    continue

            try:
                await member.timeout(
                    timedelta(minutes=moderation["time_to_mute"]),
                    reason=output["moderation"]["reason"],
                )
            except discord.Forbidden:
                print(f"Insufficient permissions to mute {message.author.name}.")
                continue

            await direct_msg(
                choice(output["moderation"]["mute"]).replace(
                    "{{MINUTES}}", str(moderation["time_to_mute"])
                ),
                message,
            )
            continue
