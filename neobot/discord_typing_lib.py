from __future__ import annotations

from discord.ext.commands import Context as dContext
from discord.channel import TextChannel
from discord.guild import Guild

class Context(dContext):

    @property
    def channel(self) -> TextChannel: ...

    @property
    def guild(self) -> Guild: ...
