from __future__ import annotations

from neobot.env import TOKEN
from neobot.bot import bot


def main() -> None:
    bot.run(TOKEN)


if __name__ == '__main__':
    main()
