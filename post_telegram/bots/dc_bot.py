# -*- coding: utf-8 -*-
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from typing import List

import requests

from post_telegram import logger
from post_telegram.bots import TelegramBot
from post_telegram.bots.utils import escape_text, Message


@dataclass(frozen=True)
class DCNews:
    """新闻信息的数据封装类"""

    id: int
    title: str
    content: str
    publish_time: int

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DCNews):
            return NotImplemented
        return self.id == other.id

    def to_markdown(self) -> str:
        return f"""
        *{escape_text(self.title)}*

{escape_text(self.content)}

{escape_text(datetime.fromtimestamp(self.publish_time / 1000, tz=timezone(timedelta(hours=8))).strftime('(%Y-%m-%d %H:%M)'))}
        """


def get_news() -> List[DCNews]:
    url = "https://api.beekuaibao.com/homepage/pcApi/news/list"
    logger.info("Query news from BeeKuaiBao")
    response = requests.get(
        url,
        params={"pageSize": 20,},
        headers={
            "User-Agent": "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:70.0) Gecko/20100101 Firefox/70.0",
            "origin": "https://www.beekuaibao.com",
            "Accept": "application/json, text/javascript, */*; q=0.01",
        },
    )
    news_list = []
    if response.status_code == 200:
        for item in response.json().get("data", []):
            news_list.append(
                DCNews(
                    id=item["id"],
                    title=item["title"],
                    content=item["content"],
                    publish_time=item["publishTime"],
                )
            )
    else:
        logger.warning("Get news failed")
        logger.error(response.text)
    return news_list


class DCBot(TelegramBot):
    def get_messages(self) -> List[Message]:
        news_list = get_news()
        # 按照时间先后排序
        messages = []
        if news_list:
            news_list.reverse()
            for news in news_list:
                messages.append(
                    Message(text=news.to_markdown(), published_at=news.publish_time)
                )
        return messages
