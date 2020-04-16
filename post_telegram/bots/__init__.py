# -*- coding: utf-8 -*-
import time
from typing import List, Optional

import requests

from post_telegram import logger
from post_telegram.bots.utils import Message


class TelegramBot:
    def __init__(self, token: str, chat_id: str, interval: Optional[int] = None):
        self.token = token
        self.chat_id = chat_id
        self.interval = interval
        self.start_time = int(time.time() * 1000)

    def _send_message(
        self, message: Message, parse_mode: str, disable_web_page_preview: bool
    ) -> None:
        response = requests.post(
            url=f"https://api.telegram.org/bot{self.token}/sendMessage",
            data={
                "chat_id": self.chat_id,
                "text": str(message),
                "parse_mode": parse_mode,
                "disable_web_page_preview": disable_web_page_preview,
            },
        )
        logger.info(response.text)

    def _bulk_send_messages(
        self, messages: List[Message], parse_mode: str, disable_web_page_preview: bool
    ) -> None:
        for message in messages:
            if self.is_message_expired(message):
                logger.info(f"Ignore expired message: {message}")
                continue
            self._send_message(message, parse_mode, disable_web_page_preview)

    def post(
        self, parse_mode: str = "MarkdownV2", disable_web_page_preview: bool = True
    ) -> None:
        messages = self.get_messages()
        self._bulk_send_messages(messages, parse_mode, disable_web_page_preview)

    def get_messages(self) -> List[Message]:
        raise NotImplementedError

    def is_message_expired(self, message: Message) -> bool:
        if self.interval is None:
            return False
        if self.start_time - self.interval * 1000 <= message.published_at:
            return False
        return True


from .cb_bot import CBBot
from .dc_bot import DCBot
from .finance_bot import FinanceBot
