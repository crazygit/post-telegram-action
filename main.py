# -*- coding: utf-8 -*-
import argparse
from typing import Optional

from post_telegram.bots import CBBot, FinanceBot, DCBot, TelegramBot


class BotFactory:
    @staticmethod
    def create_bot(
        name: str, token: str, chat_id: str, interval: Optional[int] = None
    ) -> TelegramBot:
        if name == "cb":
            cls = CBBot
        elif name == "finance":
            cls = FinanceBot
        elif name == "dc":
            cls = DCBot
        else:
            raise ValueError(f"Unknown Bot name: {name}")
        return cls(token, chat_id, interval)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Choose bot to trigger")
    parser.add_argument(
        "name", type=str, choices=["cb", "finance", "dc"], help="bot name to run"
    )
    parser.add_argument("token", type=str, help="bot token")
    parser.add_argument("chat_id", type=str, help="channel or group chat_id")
    parser.add_argument(
        "-i", "--interval", type=int, help="trigger interval in seconds", default=None
    )

    args = parser.parse_args()
    bot = BotFactory.create_bot(args.name, args.token, args.chat_id, args.interval)
    bot.post()
