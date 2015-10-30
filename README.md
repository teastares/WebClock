# Tsinghua_Course_Spider v0.1

此爬虫程序希望从清华大学网络学上获取信息并发送至指定邮箱，通过邮箱和微信的关联而使得我们能够从微信上及时收到网络学堂的更新信息。

包括：新发布的公告，新发布的作业，新上传的文件。

v0.1版本实现了基本的登录以及获取未读公告的功能，由于python2的编码复杂性问题，此脚本全部采用python3编写。

我们希望在v0.2版本中实现以下功能的一个或者几个：

1. 使用bs4重新解析网页，提升网页解析速度及代码可读性。

2. 并行化处理，在一台服务器（VPS）上同时爬取多个账号信息。

3. 使用微信公众号代替邮箱接受信息。（可选）

4. 完整的邮件发送功能。（已完成）

5. 建立每门课程的数据库。

6. 兼容新版网络学堂。

7. 搭建web客户端。（可选）

此脚本的程序结构如下：

├── db.py
├── LICENSE
├── mail.py
├── main.py
├── parse.py
├── README.md
├── resources
│   ├── account.json
│   ├── headers.json
│   ├── \__init\__.py
│   ├── mail_account.json
│   └── urls.py
└── util.py


main.py为爬虫的主程序，util.py储存了一些需要的数据结构，resources/urls.py 储存了一些需要的url。

而将用户信息（用户名和密码）储存在resources/account.json中。

