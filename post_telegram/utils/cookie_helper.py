import time

import requests.utils
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.core.os_manager import ChromeType
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options

from post_telegram import logger
from requests.cookies import RequestsCookieJar
import os


# 本地调试默认使用google-chrome浏览器，github中使用chromium浏览器
def get_chrome_driver() -> WebDriver:
    chrome_type = os.getenv("CHROME_TYPE", default="google-chrome")
    chrome_type = (
        ChromeType.CHROMIUM if chrome_type == "chromium" else ChromeType.GOOGLE
    )
    options = Options()
    # 雪球首页 onload 在低配机器上可能永远等不完，eager 到 DOMContentLoaded 即可
    options.page_load_strategy = "eager"
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-browser-side-navigation")
    # 雪球 WAF 拦截 HeadlessChrome UA 和 webdriver 特征，伪装成普通 Chrome
    options.add_argument(
        "--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36"
    )
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    return webdriver.Chrome(
        # 从这里可以下载对应版本的chromedriver及查看版本信息
        # https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json
        service=ChromeService(
            ChromeDriverManager(
                chrome_type=chrome_type
            ).install()
        ),
        options=options,
    )


# 适应于通过js set_cookie的网站进行反爬的网站，该网站一般需要请求两次才能完整获取到cookie
def get_cookies_with_twice_requests(url: str) -> RequestsCookieJar:
    driver = get_chrome_driver()
    driver.get(url)
    # eager 策略下等待反爬挑战与统计 JS 写完 cookie
    time.sleep(8)

    logger.info("=======get first cookies========")
    for cookie in driver.get_cookies():
        logger.info(f"{cookie.get('name')} = {cookie.get('value')}")

    driver.get(url)
    time.sleep(8)

    logger.info("=======get second cookies========")
    cookie_dict = {}
    for cookie in driver.get_cookies():
        logger.info(f"{cookie.get('name')} = {cookie.get('value')}")
        cookie_dict[cookie.get("name")] = cookie.get("value")
    return requests.utils.cookiejar_from_dict(cookie_dict)
