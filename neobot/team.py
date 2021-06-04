from __future__ import annotations

from traceback import print_exc
from pathlib import Path

from ruamel.yaml import YAML, yaml_object
from discord import TextChannel, VoiceChannel, CategoryChannel, Colour, PermissionOverwrite

from neobot.discord_typing import Guild, Member, Role


def permissions_for_role(guild: Guild, role: Role) -> dict[Role, PermissionOverwrite]:
    rw_perms = PermissionOverwrite(
        read_messages=True, send_messages=True, connect=True, speak=True, view_channel=True)
    no_perms = PermissionOverwrite(
        read_messages=False, send_messages=False, connect=False, speak=False, view_channel=False)
    bot_perms = PermissionOverwrite(
        read_messages=True, send_messages=True, connect=True, view_channel=True)
    perms = {
        guild.default_role: no_perms,
        role: rw_perms,
        guild.me.roles[-1]: bot_perms,
    }
    # bot_perms_d = {guild.me.roles[-1]: bot_perms,}
    return perms
    # return {role: rw_perms}


yaml = YAML(typ="safe")
yaml.indent(mapping=2, sequence=4, offset=2)
yaml.explicit_start = True
yaml.explicit_end = True

# yaml.register_class(Guild)
# yaml.register_class(Member)


@yaml_object(yaml)
class Teams:
    def __init__(self) -> None:
        self.teams: dict[Guild, dict[str, Team]] = {}
        self.players: dict[Guild, dict[Member, Team]] = {}

    def make_teams_guild_dict(self, guild: Guild) -> None:
        try:
            self.teams[guild]
        except KeyError:
            self.teams[guild] = {}

    def make_players_guild_dict(self, guild: Guild) -> None:
        try:
            self.players[guild]
        except KeyError:
            self.players[guild] = {}

    async def new_team(self, name: str, guild: Guild) -> Team:
        new = Team(name=name, guild=guild)
        self.make_teams_guild_dict(guild)

        try:
            self.teams[guild][name] = new
            await new.create()
        except KeyError:
            print_exc()
            raise

        self.save_to_file()
        return new

    async def delete_team(self, name: str, guild: Guild) -> bool:
        self.make_teams_guild_dict(guild)

        try:
            members = self.teams[guild][name].members
        except KeyError:
            return False

        for player in members:
            await self.remove_player_from_team(guild=guild, player=player)

        try:
            await self.teams[guild][name].delete()
        except:
            print_exc()
            raise

        self.teams[guild].pop(name)
        self.save_to_file()
        return True

    async def add_player_to_team(self, name: str, guild: Guild, player: Member) -> bool:

        self.make_players_guild_dict(guild)

        # Only one team at a time
        await self.remove_player_from_team(guild=guild, player=player)

        try:
            await self.teams[guild][name].add_player(player=player)
            self.players[guild][player] = self.teams[guild][name]
            self.save_to_file()
            return True
        except KeyError:
            print_exc()
            return False

    async def remove_player_from_team(self, guild: Guild, player: Member) -> bool:
        try:
            await self.players[guild].pop(player).remove_player(player)
            self.save_to_file()
            return True
        except KeyError:
            return False

    def save_to_file(self) -> None:
        dir = Teams.make_teams_dir()
        file = dir / "teams.yaml"
        with file.open("w") as f:
            yaml.dump(self, f)

    @staticmethod
    def load_from_file() -> Teams:
        dir = Teams.make_teams_dir()
        file = dir / "teams.yaml"
        if file.exists():
            with file.open("r") as f:
                return yaml.load(f)
        else:
            return Teams()

    @staticmethod
    def make_teams_dir() -> Path:
        dir = Path("data")
        if dir.exists() and dir.is_dir():
            pass
        else:
            dir.mkdir()
        return dir


teams = None


def load_teams():
    global teams
    teams = Teams.load_from_file() or Teams()
    return teams


@yaml_object(yaml)
class Team:
    """Structure contenant les informations d'une équipe"""

    def __init__(self, name: str, guild: Guild) -> None:
        self.name = name
        self.guild = guild

    async def create(self) -> None:
        self.role = await self.guild.create_role(name=self.name, hoist=True, mentionable=True, colour=Colour.random())

        self.category: CategoryChannel = await self.guild.create_category(name=self.name, overwrites=permissions_for_role(guild=self.guild, role=self.role))

        self.text: TextChannel = await self.category.create_text_channel(name=self.name)
        self.voice: VoiceChannel = await self.category.create_voice_channel(name=self.name)

        self.members = []

        # self.save_to_file()

    # def save_to_file(self) -> None:
    #     self.make_team_dir()
    #     with Path(f"{self.name}.yaml").open("w") as f:
    #         yaml.dump(self, f)

    async def delete(self) -> bool:
        # TODO: Put the right exceptions here
        try:
            await self.text.delete()
        except:
            print_exc()
            raise
        try:
            await self.voice.delete()
        except:
            print_exc()
            raise
        try:
            await self.category.delete()
        except:
            print_exc()
            raise
        try:
            await self.role.delete()
        except:
            print_exc()
            raise
        return True

    async def add_player(self, player: Member) -> bool:
        try:
            await player.add_roles(self.role)
            self.members.append(player)
            return True
        # TODO: Put the right exceptions here
        except:
            print_exc()
            raise
            # return False

    async def remove_player(self, player: Member) -> bool:
        try:
            await player.remove_roles(self.role)
        # TODO: Put the right exceptions here
        except:
            print_exc()
            raise

        try:
            self.members.remove(player)
        except ValueError:
            pass

        return True

# class Player:
#     """Structure contenant les informations d'un joueur"""
