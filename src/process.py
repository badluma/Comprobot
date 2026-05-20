import os
from random import choice

import discord
from appdirs import user_cache_dir, user_data_dir
from discord.ext import commands as ext_commands

from . import api
from . import commands as cmd_module
from . import money_system
from .bot import bot
from .data import active, ai, config, error_messages, keywords, output

from .functions import chat
from .moderation import check_message


def _is_admin_or_bot_admin():
    async def predicate(ctx):
        return (
            ctx.author.guild_permissions.administrator
            or ctx.author.id in config["bot_admins"]
        )

    return ext_commands.check(predicate)


class Comprobot(ext_commands.Cog):
    async def cog_check(self, ctx):
        if config["whitelist_mode"] and config["whitelist"]:
            allowed = config["allowed_channels"]
            channel = ctx.channel
            if isinstance(channel, discord.Thread):
                return channel.id in allowed or channel.parent_id in allowed
            return channel.id in allowed
        return True

    async def cog_before_invoke(self, ctx):
        await ctx.bot.http.send_typing(ctx.channel.id)

    # ── Commands ─────────────────────────────────────────────────────────────

    @ext_commands.command(
        name=keywords["general"]["quote"][0],
        aliases=keywords["general"]["quote"][1:],
    )
    @ext_commands.check(lambda ctx: active["general"]["quote"])
    async def quote_cmd(self, ctx):
        await ctx.send(api.quote())

    @ext_commands.command(
        name=keywords["general"]["joke"][0],
        aliases=keywords["general"]["joke"][1:],
    )
    @ext_commands.check(lambda ctx: active["general"]["joke"])
    async def joke_cmd(self, ctx):
        await ctx.send(api.joke())

    @ext_commands.command(
        name=keywords["general"]["meme"][0],
        aliases=keywords["general"]["meme"][1:],
    )
    @ext_commands.check(lambda ctx: active["general"]["meme"])
    async def meme_cmd(self, ctx):
        await ctx.send(api.meme())

    @ext_commands.command(
        name=keywords["general"]["waifu"][0],
        aliases=keywords["general"]["waifu"][1:],
    )
    @ext_commands.check(lambda ctx: active["general"]["waifu"])
    async def waifu_cmd(self, ctx):
        await ctx.send(api.waifu())

    @ext_commands.command(
        name=keywords["general"]["duck"][0],
        aliases=keywords["general"]["duck"][1:],
    )
    @ext_commands.check(lambda ctx: active["general"]["duck"])
    async def duck_cmd(self, ctx):
        await ctx.send(api.duck())

    @ext_commands.command(
        name=keywords["general"]["dog"][0],
        aliases=keywords["general"]["dog"][1:],
    )
    @ext_commands.check(lambda ctx: active["general"]["dog"])
    async def dog_cmd(self, ctx):
        await ctx.send(api.dog())

    @ext_commands.command(
        name=keywords["general"]["cat"][0],
        aliases=keywords["general"]["cat"][1:],
    )
    @ext_commands.check(lambda ctx: active["general"]["cat"])
    async def cat_cmd(self, ctx):
        await ctx.send(api.cat())

    @ext_commands.command(
        name=keywords["general"]["chuck_norris"][0],
        aliases=keywords["general"]["chuck_norris"][1:],
    )
    @ext_commands.check(lambda ctx: active["general"]["chuck_norris"])
    async def chuck_cmd(self, ctx):
        await ctx.send(api.chuck())

    @ext_commands.command(
        name=keywords["general"]["fact"][0],
        aliases=keywords["general"]["fact"][1:],
    )
    @ext_commands.check(lambda ctx: active["general"]["fact"])
    async def fact_cmd(self, ctx):
        await ctx.send(api.fact())

    @ext_commands.command(
        name=keywords["general"]["bible"][0],
        aliases=keywords["general"]["bible"][1:],
    )
    @ext_commands.check(lambda ctx: active["general"]["bible"])
    async def bible_cmd(
        self,
        ctx,
        book: str | None = None,
        chapter: int | None = None,
        verse: int | None = None,
    ):
        if book is None:
            await ctx.send(api.bible(True))
        elif chapter is not None and verse is not None:
            await ctx.send(api.bible(False, book, chapter, verse))
        else:
            await ctx.send(error_messages["missing_argument"])

    @ext_commands.command(
        name=keywords["general"]["truth"][0],
        aliases=keywords["general"]["truth"][1:],
    )
    @ext_commands.check(lambda ctx: active["general"]["truth"])
    async def truth_cmd(self, ctx, rating: str | None = None):
        result = api.tord("https://api.truthordarebot.xyz/v1/truth", rating)
        if result:
            await ctx.send(
                choice(output["general"]["truth"]).replace("{{QUESTION}}", result)
            )
        else:
            await ctx.send(error_messages["truth"])

    @ext_commands.command(
        name=keywords["general"]["dare"][0],
        aliases=keywords["general"]["dare"][1:],
    )
    @ext_commands.check(lambda ctx: active["general"]["dare"])
    async def dare_cmd(self, ctx, rating: str | None = None):
        result = api.tord("https://api.truthordarebot.xyz/api/dare", rating)
        if result:
            await ctx.send(
                choice(output["general"]["dare"]).replace("{{QUESTION}}", result)
            )
        else:
            await ctx.send(error_messages["dare"])

    @ext_commands.command(
        name=keywords["general"]["wyr"][0],
        aliases=keywords["general"]["wyr"][1:],
    )
    @ext_commands.check(lambda ctx: active["general"]["wyr"])
    async def wyr_cmd(self, ctx, rating: str | None = None):
        result = api.tord("https://api.truthordarebot.xyz/api/wyr", rating)
        if result:
            await ctx.send(
                choice(output["general"]["wyr"]).replace("{{QUESTION}}", result)
            )
        else:
            await ctx.send(error_messages["wyr"])

    @ext_commands.command(
        name=keywords["general"]["never_have_i_ever"][0],
        aliases=keywords["general"]["never_have_i_ever"][1:],
    )
    @ext_commands.check(lambda ctx: active["general"]["never_have_i_ever"])
    async def nhie_cmd(self, ctx, rating: str | None = None):
        result = api.tord("https://api.truthordarebot.xyz/api/nhie", rating)
        if result:
            await ctx.send(
                choice(output["general"]["never_have_i_ever"]).replace(
                    "{{QUESTION}}", result
                )
            )
        else:
            await ctx.send(error_messages["never-hie"])

    @ext_commands.command(
        name=keywords["general"]["paranoia"][0],
        aliases=keywords["general"]["paranoia"][1:],
    )
    @ext_commands.check(lambda ctx: active["general"]["paranoia"])
    async def paranoia_cmd(self, ctx, rating: str | None = None):
        result = api.tord("https://api.truthordarebot.xyz/api/paranoia", rating)
        if result:
            await ctx.send(
                choice(output["general"]["paranoia"]).replace("{{QUESTION}}", result)
            )
        else:
            await ctx.send(error_messages["paranoia"])

    @ext_commands.command(
        name=keywords["general"]["qr_code"][0],
        aliases=keywords["general"]["qr_code"][1:],
    )
    @ext_commands.check(lambda ctx: active["general"]["qr_code"])
    async def qr_cmd(self, ctx, link: str | None = None):
        if link:
            await ctx.send(cmd_module.qr(link))
        else:
            await ctx.send(error_messages["missing_argument"])

    @ext_commands.command(
        name=keywords["general"]["calculate"][0],
        aliases=keywords["general"]["calculate"][1:],
    )
    @ext_commands.check(lambda ctx: active["general"]["calculate"])
    async def calculate_cmd(self, ctx, *, expression: str | None = None):
        if expression:
            await ctx.send(cmd_module.calculate(expression))
        else:
            await ctx.send(error_messages["missing_argument"])

    @ext_commands.command(
        name=keywords["general"]["bitcoin"][0],
        aliases=keywords["general"]["bitcoin"][1:],
    )
    @ext_commands.check(lambda ctx: active["general"]["bitcoin"])
    async def bitcoin_cmd(self, ctx, currency: str = "usd"):
        await ctx.send(api.bitcoin(currency))

    @ext_commands.command(
        name=keywords["general"]["help"][0],
        aliases=keywords["general"]["help"][1:],
    )
    @ext_commands.check(lambda ctx: active["general"]["help"])
    async def help_cmd(self, ctx, category: str | None = None):
        await ctx.send(cmd_module.help(category))

    @ext_commands.command(
        name=keywords["general"]["ascii_art"][0],
        aliases=keywords["general"]["ascii_art"][1:],
    )
    async def ascii_cmd(self, ctx):
        await ctx.send(cmd_module.ascii())

    @ext_commands.command(
        name=keywords["general"]["currency"][0],
        aliases=keywords["general"]["currency"][1:],
    )
    @ext_commands.check(lambda ctx: active["general"]["currency"])
    async def currency_cmd(
        self,
        ctx,
        amount: str | None = None,
        from_currency: str | None = None,
        to_currency: str | None = None,
    ):
        if not all([amount, from_currency, to_currency]):
            await ctx.send(error_messages["missing_argument"])
            return

            await ctx.send(error_messages["missing_argument"])


    # ── Money ─────────────────────────────────────────────────────────────────

    @ext_commands.command(
        name=keywords["money"]["check_balance"][0],
        aliases=keywords["money"]["check_balance"][1:],
    )
    async def check_balance_cmd(self, ctx, username: str | None = None):
        if username:
            await ctx.send(money_system.check_balance(username))
        else:
            await ctx.send(error_messages["missing_argument"])

    @ext_commands.command(
        name=keywords["money"]["add_money"][0],
        aliases=keywords["money"]["add_money"][1:],
    )
    @_is_admin_or_bot_admin()
    async def add_money_cmd(
        self, ctx, username: str | None = None, amount: str | None = None
    ):
        if not username or not amount:
            await ctx.send(error_messages["missing_argument"])
            return
        try:
            await ctx.send(money_system.add_money(username, int(amount)))
        except ValueError:
            await ctx.send(f"Invalid amount: {amount}")

    @ext_commands.command(
        name=keywords["money"]["remove_money"][0],
        aliases=keywords["money"]["remove_money"][1:],
    )
    @_is_admin_or_bot_admin()
    async def remove_money_cmd(
        self, ctx, username: str | None = None, amount: str | None = None
    ):
        if not username or not amount:
            await ctx.send(error_messages["missing_argument"])
            return
        try:
            await ctx.send(money_system.remove_money(username, int(amount)))
        except ValueError:
            await ctx.send(f"Invalid amount: {amount}")

    @ext_commands.command(name="purge")
    @ext_commands.check(lambda ctx: active["general"]["purge"])
    @ext_commands.has_permissions(administrator=True)
    async def purge_cmd(self, ctx):
        await ctx.channel.purge()

    # ── Settings ──────────────────────────────────────────────────────────────

    @ext_commands.group(
        name=keywords["settings"]["settings"][0],
        aliases=keywords["settings"]["settings"][1:],
        invoke_without_command=True,
    )
    async def settings_cmd(self, ctx):
        await ctx.send(error_messages["unknown_command"])

    @settings_cmd.command(
        name=keywords["settings"]["profile_picture"][0],
        aliases=keywords["settings"]["profile_picture"][1:],
    )
    @_is_admin_or_bot_admin()
    async def pfp_cmd(self, ctx):
        if not ctx.message.attachments:
            await ctx.send(error_messages["no_attachment"])
            return
        cache_dir = user_cache_dir("Comprobot", appauthor=False)
        os.makedirs(cache_dir, exist_ok=True)
        await ctx.message.attachments[0].save(f"{cache_dir}/pfp.png")
        if bot.user is None:
            await ctx.send(error_messages["bot_unavailable"])
            return
        with open(f"{cache_dir}/pfp.png", "rb") as f:
            await bot.user.edit(avatar=f.read())
        await ctx.send(choice(output["settings"]["profile_picture_applied"]))

    @settings_cmd.command(
        name=keywords["settings"]["banner"][0],
        aliases=keywords["settings"]["banner"][1:],
    )
    @_is_admin_or_bot_admin()
    async def banner_cmd(self, ctx):
        if not ctx.message.attachments:
            await ctx.send(error_messages["no_attachment"])
            return
        cache_dir = user_cache_dir("Comprobot", appauthor=False)
        os.makedirs(cache_dir, exist_ok=True)
        await ctx.message.attachments[0].save(f"{cache_dir}/banner.png")
        if bot.user is None:
            await ctx.send(error_messages["bot_unavailable"])
            return
        with open(f"{cache_dir}/banner.png", "rb") as f:
            await bot.user.edit(banner=f.read())
        await ctx.send(choice(output["settings"]["banner_applied"]))

    @settings_cmd.command(
        name=keywords["settings"]["change_name"][0],
        aliases=keywords["settings"]["change_name"][1:],
    )
    @_is_admin_or_bot_admin()
    async def name_cmd(self, ctx, *, name: str | None = None):
        if not name:
            await ctx.send(error_messages["missing_argument"])
            return
        if bot.user is None:
            await ctx.send(error_messages["bot_unavailable"])
            return
        await bot.user.edit(username=name)
        await ctx.send(
            choice(output["settings"]["nickname_applied"]).replace("{{NAME}}", name)
        )

    @settings_cmd.command(
        name=keywords["settings"]["change_keywords"][0],
        aliases=keywords["settings"]["change_keywords"][1:],
    )
    @_is_admin_or_bot_admin()
    async def keywords_cmd(self, ctx, command_name: str | None = None, *new_keywords):
        if not command_name or not new_keywords:
            await ctx.send(error_messages["missing_argument"])
            return
        from . import data as data_module

        target_category = None
        for category in data_module.keywords:
            if command_name in data_module.keywords[category]:
                target_category = category
                break
        if target_category is None:
            await ctx.send(error_messages["unknown_argument"])
            return
        data_module.keywords[target_category][command_name] = list(new_keywords)
        data_module.save_toml(
            data_module.keywords,
            f"{user_data_dir('Comprobot')}/keywords.toml",
        )
        await ctx.send(
            choice(output["settings"]["keywords_applied"])
            .replace("{{KEYWORDS}}", " ".join(new_keywords))
            .replace("{{COMMAND}}", command_name)
        )

    # ── Events ────────────────────────────────────────────────────────────────

    @ext_commands.Cog.listener()
    async def on_message(self, message):
        print(
            "\033[90m"
            + f"[{message.channel}] "
            + "\033[36m"
            + f"{message.author.name}: "
            + "\033[0m"
            + message.content
        )

        if message.author == bot.user:
            return

        await check_message(message)

        user_id = bot.user.id if bot.user else None

        is_reply_to_bot = False
        if message.reference and message.reference.message_id and user_id:
            try:
                ref_msg = await message.channel.fetch_message(
                    message.reference.message_id
                )
                is_reply_to_bot = ref_msg.author.id == user_id
            except discord.NotFound:
                pass

        if (
            f"<@{user_id}>" in message.content
            or (is_reply_to_bot and ai["answer_to_reply"])
        ) and ai["activate_ai"]:
            async with message.channel.typing():
                response = await chat(message)
                if response:
                    content = str(response)
                    for chunk in [
                        content[i : i + 2000] for i in range(0, len(content), 2000)
                    ]:
                        await message.channel.send(chunk)

        ctx = await bot.get_context(message)
        await bot.invoke(ctx)
