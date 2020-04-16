![Post Fiance and Digital Currency News every 5 minutes](https://github.com/crazygit/post-telegram-action/workflows/Post%20Fiance%20and%20Digital%20Currency%20News%20every%205%20minutes/badge.svg)
![Post convertible boud trading message on every work day.](https://github.com/crazygit/post-telegram-action/workflows/Post%20convertible%20boud%20trading%20message%20on%20every%20work%20day./badge.svg)

## Telegam频道消息发布



### Telegram频道

* 财经资讯7x24: <https://t.me/livenews_7x24>
* 币圈资讯7x24:  <https://t.me/dc_news_7x24>
* 可转债打新: <https://t.me/cbnew>


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

3. If you use channel id, Don't forget add '@' symbole before it.


## 鸣谢

**感谢`Github action`的免费支持**
**感谢Telegram**
