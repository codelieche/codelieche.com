# codelieche.com博客

## 基本使用
1. 先创建个根目录: `mkdir codelieche.com && cd codelieche.com`
2. 把项目代码放在子目录source中: `git clone https://github.com/codelieche/codelieche.com.git source`
3. 创建数据目录:`mkdir database` 在根目录下创建database目录，数据库的文件放到这个目录中
4. 创建数据库表: `cd source && python manage.py migrate`
5. 启动服务: `python manage.py runserver`

### 目录说明:

```
codelieche.com/
├── database   数据库文件，项目的db.sqlite3文件, 生产环境用mysql数据库
├── logs       日志文件目录：项目生产环境中nginx，gunicorn访问日志文件放这里
├── source     项目代码目录：项目源代码
├── static     项目静态文件目录: 项目`python manage.py collectstatic`静态文件存放目录
└── virtualenv 项目运行环境
```

