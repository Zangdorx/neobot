from __future__ import annotations

from discord.ext.commands import Context as dContext
from discord import Guild as dGuild
from discord import Member as dMember
from discord.ext.commands import Bot as dBot
from discord import Role as dRole

from discord import TextChannel, Message, User

class Context(dContext):

    @property
    def channel(self) -> TextChannel: ...

    @property
    def guild(self) -> Guild: ...

    @property
    def message(self) -> Message: ...

    @property
    def author(self) -> Member: ...

class Guild(dGuild):
    
    @property
    def default_role(self) -> Role: ...

    @property
    def me(self) -> Member: ...

    def get_member(self, user_id) -> Member: ...

    async def create_role(self, *, **fields) -> Role: ...

class Member(dMember):

    @property
    def _user(self) -> User: ...

    @property
    def guild(self) -> Guild: ...

    @property
    def roles(self) -> list[Role]: ...

class Bot(dBot):

    def get_guild(self, id) -> Guild: ...


class Role(dRole):

    @property
    def guild(self) -> Guild: ...
