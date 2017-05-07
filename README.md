# codelieche.com博客

## 基本使用
1. 先创建个根目录: `mkdir codelieche.com && cd codelieche.com`
2. 把项目代码放在子目录source中: `git clone https://github.com/codelieche/codelieche.com.git source`
3. 创建数据目录:`mkdir database` 在根目录下创建database目录，数据库的文件放到这个目录中
4. 创建数据库表: `cd source && python manage.py migrate`
5. 启动服务: `python manage.py runserver`
6. 自己创建管理员用户: `python manage.py createsuperuser`
7. 添加测试数据

### 目录说明:

```
codelieche.com/
├── database   数据库文件，项目的db.sqlite3文件, 生产环境用mysql数据库
├── logs       日志文件目录：项目生产环境中nginx，gunicorn访问日志文件放这里
├── source     项目代码目录：项目源代码
├── static     项目静态文件目录: 项目`python manage.py collectstatic`静态文件存放目录
└── virtualenv 项目运行环境
```


## 项目发布

### 环境准备
1. 服务器，系统是debian或者ubuntu，其它流程一样，代码需要微调
2. 服务器上，手动安装python开发环境
3. 安装好nginx和supervisor

### 部署项目
1. 进入deploy_tools: `cd deploy_tools`
1. 部署代码到服务器: `fab -H user@192.168.1.123 deploy`
    > 部署代码到服务器，注意user需要拥有对`/data/www`目录的读写权限

1. 配置nginx和supervisor: `fab -H user@192.168.1.123 deploy_settings`
    > 需要用到sudo，需要输入用户密码，而且需要有sudo的权限。

1. 手动去reload nginx和启动supervisor任务，有问题先单独运行`../run.sh`脚本试试看
    > sudo service nginx reload && sudo supervisorctl start codelieche

