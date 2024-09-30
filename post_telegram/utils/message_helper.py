# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import Dict

import requests

from post_telegram import logger


@dataclass(frozen=True)
class Message:
    text: str
    published_at: int  # 毫秒

    def __repr__(self) -> str:
        return self.text


def format_cell(cell: Dict[str, str]) -> str:
    lucky_draw_rt = (
        escape_text(cell["lucky_draw_rt"]) + "%"
        if cell["lucky_draw_rt"]
        else escape_text("---")
    )
    return f"""
    名   称: {escape_text(cell["stock_nm"] + '(' + cell["bond_nm"] + ')')}
    债券代码: [{cell["bond_id"]}](https://www.jisilu.cn/data/convert_bond_detail/{cell["bond_id"]})
    证券代码: [{cell["stock_id"]}](https://www.jisilu.cn/data/stock/{cell["stock_id"]})
    现    价: {escape_text(cell["price"])}
    中签率: {lucky_draw_rt}
    评   级: {escape_text(cell["rating_cd"])}
    申购建议: {escape_text(cell["jsl_advise_text"])}
    """


def escape_text(text: str) -> str:
    if text:
        for keyword in [
            "_",
            "*",
            "[",
            "]",
            "(",
            ")",
            "~",
            "`",
            ">",
            "#",
            "+",
            "-",
            "=",
            "|",
            "{",
            "}",
            ".",
            "!",
        ]:
            text = text.replace(keyword, f"\\{keyword}")
        return text
    return ""


# refer: https://core.telegram.org/bots/api#sendmessage
def send_message(token: str, chat_id: str, message: dict) -> None:
    logger.info(message)
    response = requests.post(
        url=f"https://api.telegram.org/bot{token}/sendMessage",
        data={
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "MarkdownV2",
            "disable_web_page_preview": True,
        },
    )
    logger.info(response.text)
