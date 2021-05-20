from __future__ import annotations
import asyncio

from functools import wraps

from discord import Intents
from discord.ext.commands import Bot
from discord.guild import Guild

from neobot.context import Context
from neobot.env import DEV_GUILD_ID


intents: Intents = Intents.default()
intents.members = True

bot = Bot(command_prefix='!', intents=intents)

TEST_GUILD = None

def indev(func):

    @wraps(func)
    async def wrapper(ctx: Context) -> None:
        if ctx.guild != TEST_GUILD:
            await ctx.send("# Commande en développement -> non disponible #")
            return
        else:
            await ctx.send("# Commande en développement #")
            await func(ctx)
            return

    return wrapper


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    global TEST_GUILD
    TEST_GUILD = bot.get_guild(int(DEV_GUILD_ID))


@bot.command(name="test", help="Teste la connection du bot à Discord")
async def hello_world(ctx: Context) -> None:
    async with ctx.channel.typing():
        await ctx.send("Bonjour le monde!")


@bot.command(name="testdev", help="Teste le mode développement")
@indev
async def hello_world_dev(ctx: Context) -> None:
    async with ctx.channel.typing():
        await ctx.send("Bonjour le monde de dev!")
