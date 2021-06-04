from __future__ import annotations

from typing import Optional, Any

from ruamel.yaml import add_constructor, add_representer, Node, YAML
from ruamel.yaml.dumper import Dumper
from ruamel.yaml.loader import Loader
from ruamel.yaml.constructor import RoundTripConstructor, SafeConstructor
from ruamel.yaml.representer import RoundTripRepresenter, SafeRepresenter
from discord import CategoryChannel, TextChannel, VoiceChannel

from neobot.discord_typing import Guild, Member, Bot, Role

class BotLoader():

    def __init__(self, bot: Bot) -> None:
        self.bot = bot

        representer=SafeRepresenter
        constructor=SafeConstructor

        add_representer(Guild, self.dump_guild, representer=representer)
        add_representer(Member, self.dump_member, representer=representer)
        add_representer(Role, self.dump_role, representer=representer)
        add_representer(CategoryChannel, self.dump_category_channel, representer=representer)
        add_representer(TextChannel, self.dump_text_channel, representer=representer)
        add_representer(VoiceChannel, self.dump_voice_channel, representer=representer)

        add_constructor("!tag:discord.py:Guild", self.load_guild, constructor=constructor)
        add_constructor("!tag:discord.py:Member", self.load_member, constructor=constructor)
        add_constructor("!tag:discord.py:Role", self.load_role, constructor=constructor)
        add_constructor("!tag:discord.py:CategoryChannel", self.load_channel, constructor=constructor)
        add_constructor("!tag:discord.py:TextChannel", self.load_channel, constructor=constructor)
        add_constructor("!tag:discord.py:VoiceChannel", self.load_channel, constructor=constructor)

    def dump_guild(self, dumper: Dumper, guild: Guild):
        return dumper.represent_mapping("!tag:discord.py:Guild", {"id": guild.id})

    def dump_member(self, dumper: Dumper, member: Member):
        return dumper.represent_mapping("!tag:discord.py:Member", {"user_id": member._user.id, "guild_id": member.guild.id})

    def dump_role(self, dumper: Dumper, role: Role):
        return dumper.represent_mapping("!tag:discord.py:Role", {"role_id": role.id, "guild_id": role.guild.id})

    def dump_category_channel(self, dumper: Dumper, category_channel: CategoryChannel):
        return dumper.represent_mapping("!tag:discord.py:CategoryChannel", {"channel_id": category_channel.id, "guild_id": category_channel.guild.id})

    def dump_text_channel(self, dumper: Dumper, text_channel: TextChannel):
        return dumper.represent_mapping("!tag:discord.py:TextChannel", {"channel_id": text_channel.id, "guild_id": text_channel.guild.id})

    def dump_voice_channel(self, dumper: Dumper, voice_channel: VoiceChannel):
        return dumper.represent_mapping("!tag:discord.py:VoiceChannel", {"channel_id": voice_channel.id, "guild_id": voice_channel.guild.id})

    def load_guild(self, loader: Loader, node: Node):
        map = loader.construct_mapping(node)
        a = self.bot.get_guild(int(map["id"]))
        return a

    def load_member(self, loader: Loader, node: Node):
        map = loader.construct_mapping(node)
        a = self.bot.get_guild(int(map["guild_id"])).get_member(int(map["user_id"]))
        return a

    def load_role(self, loader: Loader, node: Node):
        map = loader.construct_mapping(node)
        a = self.bot.get_guild(int(map["guild_id"])).get_role(int(map["role_id"]))
        return a

    def load_channel(self, loader: Loader, node: Node):
        map = loader.construct_mapping(node)
        a = self.bot.get_guild(int(map["guild_id"])).get_channel(int(map["channel_id"]))
        return a

    # def load_text_channel(self, loader: Loader, node: Node):
    #     return self.bot.get_guild(int(node.value["guild_id"])).get_role(int(node.value["role_id"]))

    # def load_voice_channel(self, loader: Loader, node: Node):
    #     return self.bot.get_guild(int(node.value["guild_id"])).get_role(int(node.value["role_id"]))
