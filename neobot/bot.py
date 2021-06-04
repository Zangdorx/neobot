from __future__ import annotations

from functools import wraps, WRAPPER_ASSIGNMENTS, WRAPPER_UPDATES
from neobot.args_parsing import ArgumentParser, MissingArgumentsError, Namespace
from traceback import print_exc
from typing import Callable, Coroutine, Any, Union
from typing_extensions import TypeAlias
from types import MethodType

from discord import Intents
from discord.ext.commands import Command

from neobot.discord_typing import Context, Guild, Bot
from neobot.env import DEV_GUILD_ID
from neobot.team import Teams
from neobot.team import load_teams
from neobot.discord_yaml import BotLoader


intents: Intents = Intents.default()
intents.members = True

bot = Bot(command_prefix='!', intents=intents)
async def on_command_error(self, context, exception):
    await context.send(str(exception))
bot.on_command_error = MethodType(on_command_error, bot)

TEST_GUILD = None
BOT_LOADER = None
COMMANDS = None


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    global TEST_GUILD
    global BOT_LOADER
    global COMMANDS
    TEST_GUILD = bot.get_guild(int(DEV_GUILD_ID))
    BOT_LOADER = BotLoader(bot)
    COMMANDS = BotCommands(bot, load_teams()).register_commands()

command_coro: TypeAlias = Callable[[
    'BotCommands', Context], Coroutine[Any, Any, Any]]


def indev(func: command_coro) -> command_coro:

    # @wraps(func, assigned=['__name__'])
    @wraps(func)
    async def wrapper(self, ctx: Context, *args, **kwargs) -> None:
        if ctx.guild != TEST_GUILD:
            await ctx.send("# Commande en développement -> non disponible #")
            return
        else:
            await func(self, ctx)
            return

    return wrapper


command_parser_coro: TypeAlias = Callable[[
    'BotCommands', ArgumentParser, Context], Coroutine[Any, Any, Any]]

WRAPPER_ASSIGNMENTS_DROP_ANNOTATIONS = tuple(
    i for i in WRAPPER_ASSIGNMENTS if i != '__annotations__')


def withparser(func: command_parser_coro) -> command_coro:

    # @wraps(func, assigned=WRAPPER_ASSIGNMENTS_DROP_ANNOTATIONS)
    # @wraps(func)
    async def wrapper(self, ctx: Context, *args, **kwargs) -> None:
        parser = ArgumentParser(func.__qualname__)
        return await func(self, parser, ctx)

    wrapper.__name__ = func.__name__ 
    wrapper.__qualname__ = func.__qualname__ 
    wrapper.__doc__ = func.__doc__
    try:
        wrapper.__dict__['params'] = func.__dict__['params']
    except:
        pass
    return wrapper


def parse_from_str(text: str, parser: ArgumentParser) -> Union[str, Namespace]:

    try:
        args = text.split(maxsplit=1)[1:]
        args = parser.parse_args(args)
    except MissingArgumentsError as e:
        return f"[Mauvais arguments] {str(e)}"

    return args


commands = []


def command(*cargs, **ckwargs):
    def decorator(func: command_coro) -> command_coro:
        global commands
        commands.append((func, cargs, ckwargs))

        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            return await func(self, *args, **kwargs)
        return wrapper
    return decorator


class BotCommands:

    def __init__(self, bot: Bot, teams: Teams) -> None:
        self.teams = teams
        self.bot = bot
        global commands
        self.commands = commands

    def register_commands(self):
        for command in self.commands:
            try:
                self.bot.add_command(
                    Command(eval(f"self.{command[0].__name__}"), *command[1], **command[2]))
            except:
                pass
        return self

    @command(name="test", help="Teste la connection du bot à Discord")
    async def hello_world(self, ctx: Context) -> None:
        async with ctx.channel.typing():
            await ctx.send("Bonjour le monde!")

    @command(name="testdev", help="Teste le mode développement")
    @indev
    async def hello_world_dev(self, ctx: Context) -> None:
        async with ctx.channel.typing():
            await ctx.send("Bonjour le monde de dev!")

    @command(name="mkteam", help="Crée une équipe avec le nom donné et une couleur aléatoire")
    @indev
    @withparser
    async def cmd_mkteam(self, parser: ArgumentParser, ctx: Context, *args, **kwargs) -> None:
        parser.add_argument("team_name", type=str)
        args = parse_from_str(ctx.message.content, parser)

        if isinstance(args, str):
            await ctx.send(args)
            return

        try:
            await self.teams.new_team(args.team_name, ctx.guild)
        except:
            print_exc()
            raise

    @command(name="rmteam", help="Supprime l'équipe avec le nom donné")
    @indev
    @withparser
    async def cmd_rmteam(self, parser: ArgumentParser, ctx: Context) -> None:
        parser.add_argument("team_name", type=str)
        args = parse_from_str(ctx.message.content, parser)

        if isinstance(args, str):
            await ctx.send(args)
            return

        try:
            await self.teams.delete_team(args.team_name, ctx.guild)
        except:
            print_exc()
            raise

    @command(name="jointeam", help="Rejoint l'équipe avec le nom donné")
    @indev
    @withparser
    async def cmd_jointeam(self, parser: ArgumentParser, ctx: Context) -> None:
        parser.add_argument("team_name", type=str)
        args = parse_from_str(ctx.message.content, parser)

        if isinstance(args, str):
            await ctx.send(args)
            return

        try:
            await self.teams.add_player_to_team(name=args.team_name, guild=ctx.guild, player=ctx.author)
        except:
            print_exc()
            raise

    @command(name="leaveteam", help="Quitte son équipe actuelle")
    @indev
    async def cmd_leaveteam(self, ctx: Context) -> None:

        try:
            await self.teams.remove_player_from_team(guild=ctx.guild, player=ctx.author)
        except:
            print_exc()
            raise
