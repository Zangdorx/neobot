from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from neobot.discord_typing_lib import Context
    from neobot.discord_typing_lib import Guild
    from neobot.discord_typing_lib import Member
    from neobot.discord_typing_lib import Bot
    from neobot.discord_typing_lib import Role
else:
    from discord.ext.commands import Context
    from discord import Guild
    from discord import Member
    from discord.ext.commands import Bot
    from discord import Role
