# -*- coding: utf-8 -*-
import datetime
import logging
import os
from typing import Tuple, List, Dict

import requests

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


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


# refer: https://core.telegram.org/bots/api#sendmessage
def send_message(token, chat_id) -> None:
    text = get_message_text()
    logger.info(text)
    response = requests.post(
        url=f"https://api.telegram.org/bot{token}/sendMessage",
        data={
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "MarkdownV2",
            "disable_web_page_preview": True,
        },
    )
    logger.info(response.text)


def main() -> None:
    token = os.getenv("TELEGRAM_TOKEN", None)
    chat_id = os.getenv("TELEGRAM_TO", None)
    assert token is not None, "Please set TELEGRAM_TOKEN env"
    assert chat_id is not None, "Please set TELEGRAM_TO env"
    logger.info(f"token: {token}")
    logger.info(f"chat_id: {chat_id}")
    send_message(token, chat_id)


if __name__ == "__main__":
    main()
