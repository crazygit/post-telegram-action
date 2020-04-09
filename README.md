![Post convertible boud trading message on every work day.](https://github.com/crazygit/post-cb-action/workflows/Post%20convertible%20boud%20trading%20message%20on%20every%20work%20day./badge.svg?branch=master&event=push)
## 打新债信息通知机器人

### 环境初始化

```bash
$ python -V
Python 3.7.0

# 安装依赖
$ pip install -r requirements.txt

# 运行服务,需要替换自己的chat_id和bot_token
$ TELEGRAM_TO="your_chat_id" TELEGRAM_TOKEN="yourt_bot_token" python postman.py
```

### 数据来源

* [集思录](https://www.jisilu.cn/data/cbnew/#pre)


### Telegram Channel

<https://t.me/cbnew>


### 如何获取chat_id

参考: <https://stackoverflow.com/a/50661601/1957625>

1. Invite `@getidsbo` or `@RawDataBot` to your group and get your group id in sended chat id field.

        Message
        ├ message_id: 338
        ├ from
        ┊  ├ id: *****
        ┊  ├ is_bot: false
        ┊  ├ first_name: 사이드
        ┊  ├ username: ******
        ┊  └ language_code: en
        ├ chat
        ┊  ├ id: -1001118554477    // This is Your Group id
        ┊  ├ title: Test Group
        ┊  └ type: supergroup
        ├ date: 1544948900
        └ text: A
2. Get from web page
    1. Goto (https://web.telegram.org)
    2. Goto your Gorup and Find your link of Gorup(https://web.telegram.org/#/im?p=g154513121)
    3. Copy That number after g and put a (-) Before That -154513121
    4. Send Your Message to Gorup bot.sendMessage(-154513121, "Hi")

