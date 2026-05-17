import asyncio
import inspect
import sys
from typing import Any, cast

from discord.ext import commands as ext_commands

from .data import config
from .process import Comprobot


class _FakeHTTP:
    async def send_typing(self, _):
        pass


class _FakePermissions:
    administrator = True


class _FakeAuthor:
    id = 0
    name = "tester"
    guild_permissions = _FakePermissions()


class _FakeChannel:
    id = 0

    async def purge(self):
        pass


class _FakeBotUser:
    id = 1


class _FakeBot:
    http = _FakeHTTP()
    user = _FakeBotUser()


class _FakeMessage:
    attachments = []
    reference = None


class _FakeCtx:
    def __init__(self):
        self.author = _FakeAuthor()
        self.channel = _FakeChannel()
        self.message = _FakeMessage()
        self.bot = _FakeBot()

    async def send(self, content):
        print(content)


def _find_command(cog, parts):
    """Return (command, remaining_args) or (None, [])."""
    if not parts:
        return None, []

    cmd_name = parts[0].lower()
    remaining = parts[1:]

    for command in cog.__cog_commands__:
        if command.parent is not None:
            continue
        names = [command.name] + list(command.aliases or [])
        if cmd_name not in names:
            continue
        if isinstance(command, ext_commands.Group) and remaining:
            sub = command.all_commands.get(remaining[0].lower())
            if sub:
                return sub, remaining[1:]
        return command, remaining

    return None, []


async def _run(message: str) -> int:
    prefix = config.get("prefix", "!")
    if not message.startswith(prefix):
        print(f"Error: message must start with prefix '{prefix}'")
        return 1

    parts = message[len(prefix) :].split()
    if not parts:
        print("Error: empty command")
        return 1

    cog = Comprobot()
    ctx: Any = _FakeCtx()
    await cog.cog_before_invoke(ctx)

    command, args = _find_command(cog, parts)
    if command is None:
        print(f"Error: unknown command '{parts[0]}'")
        return 1

    sig = inspect.signature(command.callback)
    params = list(sig.parameters.values())[2:]  # skip self, ctx
    kw_only = [p for p in params if p.kind == inspect.Parameter.KEYWORD_ONLY]

    fn = cast(Any, command.callback)
    try:
        if kw_only and args:
            await fn(cog, ctx, **{kw_only[0].name: " ".join(args)})
        else:
            await fn(cog, ctx, *args)
    except Exception as e:
        print(f"Error: {e}")
        return 1

    return 0


def run_test(message: str) -> None:
    import io

    if isinstance(sys.stdout, io.TextIOWrapper):
        sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(asyncio.run(_run(message)))
