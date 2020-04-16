# -*- coding: utf-8 -*-
import datetime
import time
from typing import Tuple, List

import requests

from post_telegram import logger
from post_telegram.bots import TelegramBot
from post_telegram.bots.utils import format_cell, escape_text, Message


def get_cb_info() -> Tuple[List, List]:
    url = "https://www.jisilu.cn/data/cbnew/pre_list/"
    response = requests.post(
        url,
        data={"cb_type_Y": "Y", "progress": "", "rp": 22},
        headers={
            "Origin": "https://www.jisilu.cn",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://www.jisilu.cn/data/cbnew/",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
        },
    )
    apply_cb = []
    listed_cb = []

    for row in response.json()["rows"]:
        cell = row["cell"]
        today = datetime.date.today().isoformat()
        # 当日可申购债券
        if cell["apply_date"] == today:
            apply_cb.append(cell)
        # 当日上市债券
        elif cell["list_date"] == today:
            listed_cb.append(cell)
    return apply_cb, listed_cb


def get_message_text() -> str:
    today = datetime.date.today().isoformat()
    logger.info(f"get message at {today}")
    apply_cb, listed_cb = get_cb_info()
    text = ""
    text += f"*日期*: {escape_text(today)}\n\n"
    if apply_cb:
        text += "*当日可打新债*: \n"
        for cell in apply_cb:
            text += format_cell(cell)
    else:
        text += "*当日无可打新债*"
    text += "\n\n"
    if listed_cb:
        text += "*当日上市新债*: \n"
        for cell in listed_cb:
            text += format_cell(cell)
    else:
        text += "*当日无上市新债*\n\n"
    text += "\n_以上数据来源于互联网，仅供参考，不作为投资建议_ "
    return text


class CBBot(TelegramBot):
    def get_messages(self) -> List[Message]:
        return [Message(text=get_message_text(), published_at=int(time.time() * 1000))]
