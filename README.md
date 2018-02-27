# looncode懒人编程

[looncode.com](http://looncode.com)

编程自学资源汇总站点。looncode就第一个web开发的全栈DEMO.这个项目的目标是让编程初学者以更低的成本获取更全面的编程入门资源。包含了编程初学者需要的自学视频资源、书籍资源、和优秀的学习站点导航功能。

我第一次学习编程在买了一本书就跟着细度和写代码，学习了2个月啥项目也写出来，最后放弃了。时隔3年，我第2次学习编程，我体验到了前所以为的乐趣。
这一次我先找了沿用了PM的习惯，预览职业方向 ->制定线路图 -> 对知识体系全局认识，有需求->再写项目->驱动学习，这次可能是真的入了门我的神啊。



# 版本和功能

v4.0（计划中）

- 职业技术树展示，结合招聘数据分析(计划阶段)

v3.0 
- 会员系统，注册登录功能，记录兑换记录功能。
- 全站VIP会员功能。vip会员解锁所有视频、书籍资源信息。

v2.0：
- 增加学习数据推荐清单。
- 增加好站点导航。
- 增加移动端适配，单独的移动端前端设计和开发。

v1.0:

- 网上可以搜索到的学习视频资源的分类聚合，不同方向资源。
- 兑换码机制，视频学习资源存储在百度云，采用专题课程激活码，解锁展示链接和提取密码。
- 免登陆，用户获取兑换码后，第一次兑换之后，写入cookies保存兑换记录，记住用户兑换记录。



# 演示站点和截图

[looncode.com](http://looncode.com) 或 百度 懒人编程


[![9BNUf0.png](https://s1.ax1x.com/2018/02/27/9BNUf0.png)](https://imgchr.com/i/9BNUf0)

# 技术栈

开发：
Flask + Redis + Sqlite3  + materializecss

- Flask为基础框架，个人全栈开发，使用非RESTful不分离方式。
- 基于jinja2模板渲染
- 使用SQLAlchemy ORM 管理 SQLite3，进行增删改查
- 使用Redis缓存。作为View视图缓存和部分model层数据缓存，提高网站可承受访问量
- PC前端采用materializecss框架(UI定制版本的bootstarp)进行布局和设计，和部分JS,
- 移动版前端采用AmazeUI作为布局和设计

部署：
Centos + Nginx + Gunicorn(gevent) + yhook

- Centos7 + Nginx 为主要运行环境
- Gunicorn(gevent) 提高并发量
- yhook为自写的自动部署服务脚本，利用github webhook，运行服务器自动监控源码，有push更新自动重启服务器web服务


# 项目目录说明

```

defland@MBP ~/W/P/r/looncode> tree -L 3                                                      11 dev!?
.
├── README.md
└── serve
    ├── application
    │   ├── __init__.py 
    │   ├── config # 项目配置文件
    │   ├── db # SQLite3数据库db文件
    │   ├── dev_tools.py # 开发调试扩展工具包(版本标记、数据打印等)
    │   ├── doc # 相关项目设计文档、API文档
    │   ├── initdb.py # 数据库初始化脚本
    │   ├── middleware.py # 中间件层
    │   ├── model.py # Model层 ，使用SQLAlchemy ORM 管理 SQLite3
    │   ├── static  # 静态资源
    │   ├── templates  # 采用模板渲染，暂时没有采用RESTful API
    │   ├── view.py  # view视图函数
    ├── gunicorn_config  # gunicorn(gevent)部署的环境配置文件
    │   ├── gunconf_dev.py
    │   ├── gunconf_local.py
    │   └── gunconf_stable.py 
    └── runserver.py # 程序部署执行入口
    
```


