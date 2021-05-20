from __future__ import annotations

from discord.ext.commands import Context as dContext
from discord.channel import TextChannel

class Context:
    def __init__(self, ctx: dContext) -> None:
        self.ctx = ctx

    @property
    def channel(self) -> TextChannel:
        return self.ctx.channel  # type: ignore

    def send(self, *args, **kwargs):
        return self.ctx.send(*args, **kwargs)
