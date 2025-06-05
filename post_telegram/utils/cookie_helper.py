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
    chrome_type = ChromeType.CHROMIUM if chrome_type == "chromium" else ChromeType.GOOGLE
    options = Options()
    options.add_argument('--headless=new')
    return webdriver.Chrome(
        # 从这里可以下载对应版本的chromedriver及查看版本信息
        # https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json
        service=ChromeService(ChromeDriverManager(chrome_type=chrome_type, driver_version="136.0.7103.113").install()),
        options=options
    )


# 适应于通过js set_cookie的网站进行反爬的网站，该网站一般需要请求两次才能完整获取到cookie
def get_cookies_with_twice_requests(url: str) -> RequestsCookieJar:
    driver = get_chrome_driver()
    driver.get(url)

    logger.info("=======get first cookies========")
    for cookie in driver.get_cookies():
        logger.info(f"{cookie.get('name')} = {cookie.get('value')}")

    driver.get(url)

    logger.info("=======get second cookies========")
    cookie_dict = {}
    for cookie in driver.get_cookies():
        logger.info(f"{cookie.get('name')} = {cookie.get('value')}")
        cookie_dict[cookie.get('name')] = cookie.get('value')
    return requests.utils.cookiejar_from_dict(cookie_dict)
