# -*- coding:utf-8 -*-
from __future__ import absolute_import

from fabric.api import env, run
from fabric.context_managers import cd

from deploy_jobs import (
    _create_directory_structure_if_necessary,
    _get_latest_source,
    _update_settings,
    _update_virtualenv,
    _update_static_files,
    _update_database,
    _inpute_value,
)

SITE_NAME = 'codelieche.com'


def deploy():
    """项目代码发布"""
    # site_folder = '/home/%s/sites/%s' % (env.user, SITE_NAME)
    site_folder = '/data/www/%s' % SITE_NAME
    source_folder = site_folder + '/source'

    # 第1步: 创建目录结构
    _create_directory_structure_if_necessary(site_folder)
    # 第2步：拉取最新源码
    _get_latest_source(source_folder)
    # 第3步：修改项目配置信息
    _update_settings(source_folder, SITE_NAME)
    # 第4步: 更新虚拟环境
    _update_virtualenv(source_folder)
    # 第5步：更新静态文件
    _update_static_files(source_folder)
    # 第6步：更新数据库
    _update_database(source_folder)


def deploy_settings():
    """项目发布-服务器配置"""
    # run('sudo supervisorctl status codelieche')
    # site_folder = '/home/%s/sites/%s' % (env.user, SITE_NAME)
    site_folder = '/data/www/%s' %(SITE_NAME)
    source_folder = site_folder + '/source'
    # 第一步：写入nginx的配置
    with cd(source_folder):
        # 进入source_folder
        run('pwd')
        run('sed "s/SITENAME/%s/g" deploy_tools/nginx.template.conf | '
            'sed "s/USERNAME/%s/g" | sudo tee /etc/nginx/sites-enabled/%s' % (
                SITE_NAME, env.user, SITE_NAME))
    # 第二步: 写入gunicorn执行脚本
    with cd(source_folder):
        # 进入source_folder
        run('sed "s/SITENAME/%s/g" deploy_tools/gunicorn-run.template.sh | '
            'sed "s/USERNAME/%s/g" | tee ../run.sh' % (
                SITE_NAME, env.user))
        # 修改run.sh的权限
        run('chmod +x ../run.sh')

    # 第三步：添加supervisor配置
    with cd(source_folder):
        # 进入source_folder
        mysql_db_name = _inpute_value("请输入网站使用的数据库名:")
        mysql_user = _inpute_value("请输入mysql数据库用户名:")
        mysql_password = _inpute_value("请输入mysql数据库密码:")
        # print(mysql_user, mysql_password)
        run('sed "s/SITENAME/%s/g" deploy_tools/gunicorn-supervisor.template.conf | '
            'sed "s/USERNAME/%s/g" | sed "s/MYSQL_USER_VALUE/%s/g" | '
            'sed "s/MYSQL_PASSWORD_VALUE/%s/g" | sed "s/MYSQL_DB_NAME_VALUE/%s/g" | '
            'sudo tee /etc/supervisor/conf.d/%s.conf' % (
                SITE_NAME, env.user, mysql_user, mysql_password, mysql_db_name, SITE_NAME))


def reload():
    """重启服务"""
    run('sudo supervisorctl restart codelieche')


def hello():
    print('Hello fab!')
