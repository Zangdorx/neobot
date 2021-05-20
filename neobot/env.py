from __future__ import annotations

import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
DEV_GUILD_ID = int(os.getenv('DISCORD_TEST_GUILD_ID')) # type: ignore
