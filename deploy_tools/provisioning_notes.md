配置新网站
========

## 需要安装的包：
- nginx
- Python 3
- Git
- pip
- virtualenv

以Ubuntu为例，可以执行下面的命令安装：

```
sudo apt-get install nginx git python3 python3-pip
sudo pip3 install virtualenv
```

## 配置Nginx虚拟机
- 参考nginx.template.conf
- 把SITENAME替换成所需的域名，例如：staging.my-domain.com
- 把USERNAME替换成所需的用户名

## Supervisor任务

- 参考gunicorn-supervisor.template.conf
- 把SITENAME替换成所需的域名，例如：staging.my-domian.com
- 把USERNAME替换成所需的用户名

## 文件夹结构：

假设有用户账号，对目录/data/www有写入的权限

```
/data/www
 |____ SITENAME
        |____ database
        |____ source
        |____ static
        |____ virtualenv
```
