# -*- coding: utf-8 -*-
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from typing import List

import requests
from requests.cookies import RequestsCookieJar

from post_telegram import logger
from post_telegram.bots import TelegramBot
from post_telegram.utils.message_helper import escape_text, Message

from post_telegram.utils.cookie_helper import get_cookies_with_twice_requests


@dataclass(frozen=True)
class FinanceNews:
    """新闻信息的数据封装类"""

    id: int
    text: str
    mark: int
    target: str = field(repr=False)
    created_at: int

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, FinanceNews):
            return NotImplemented
        return self.id == other.id

    def to_markdown(self) -> str:
        return f"""
{escape_text(self.text)}

{escape_text(datetime.fromtimestamp(self.created_at / 1000, tz=timezone(timedelta(hours=8))).strftime('(%Y-%m-%d %H:%M)'))}
"""


class FinanceBot(TelegramBot):
    requests_headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "Referer": "https://xueqiu.com",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
    }

    def get_messages(self) -> List[Message]:
        news_list = self.get_news()
        messages = []
        if news_list:
            # 按照时间先后排序
            news_list.reverse()
            for news in news_list:
                messages.append(
                    Message(text=news.to_markdown(), published_at=news.created_at)
                )
        return messages

    @classmethod
    def get_news(cls) -> List[FinanceNews]:
        url = "https://xueqiu.com/v4/statuses/public_timeline_by_category.json"
        logger.info("Query news from XueQiu")
        response = requests.get(
            url,
            params={"since_id": -1, "max_id": -1, "count": 10, "category": 6},
            headers=cls.requests_headers,
            cookies=cls.get_cookie(),
        )
        news_list = []
        if response.status_code == 200:
            for item in response.json().get("list", []):
                item = json.loads(item["data"])
                news_list.append(
                    FinanceNews(
                        id=item["id"],
                        text=item["text"],
                        mark=item["mark"],
                        target=item["target"],
                        created_at=item["created_at"],
                    )
                )
        else:
            logger.warning("Get news failed")
            logger.error(response.text)
        return news_list

    @classmethod
    def get_cookie(cls) -> RequestsCookieJar:
        return get_cookies_with_twice_requests("https://xueqiu.com")
