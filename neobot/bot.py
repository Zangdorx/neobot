from __future__ import annotations

import os
import sys
from threading import ThreadError
from dotenv import load_dotenv

from discord import Intents
from discord.ext.commands import Bot
from neobot.discord_typing_lib import Context

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
DEV_GUILD_ID = os.getenv('DISCORD_TEST_GUILD_ID')
PERMS = os.getenv('DISCORD_PERMS_INTEGER')

intents: Intents = Intents.default()
intents.members = True

bot = Bot(command_prefix='!', intents=intents)

test_guild = bot.get_guild(692122064219406376)


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(name="test", help="Teste la connection du bot à Discord")
async def hello_world(ctx: Context) -> None:
    async with ctx.channel.typing():
        await ctx.send("Bonjour le monde!")


def main() -> None:
    bot.run(TOKEN)


if __name__ == '__main__':
    main()
