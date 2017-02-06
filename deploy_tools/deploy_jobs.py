#coding:utf-8
import random

from fabric.api import run, local
from fabric.contrib.files import append, exists, sed


REPO_URL = 'https://github.com/codelieche/codelieche.com.git'

def _create_directory_structure_if_necessary(site_folder):
    '''创建发布项目的文件目录'''
    for subfolder in ('database', 'static', 'virtualenv', 'source', 'logs'):
        folder = '%s/%s' % (site_folder, subfolder)
        if not exists(folder):
            run('mkdir -p %s' % folder)
        else:
            print('目录已经存在: %s' % folder)


def _get_latest_source(source_folder):
    if exists(source_folder + '/.git'):
        print('git fetch: new code source')
        run('cd %s && git fetch' % (source_folder,))
    else:
        print('git 代码不存在，clone')
        run('git clone %s %s' % (REPO_URL, source_folder))
    # 检查本地代码的最新commit， 服务器端reset成最新的代码
    current_commit = local('git log -n 1 --format=%H', capture=True)
    run('cd %s && git reset --hard %s' % (source_folder, current_commit))

def _update_settings(source_folder, site_name):
    '''修改服务器端的配置信息:
        1. 修改: DEBUG = False
        2. 修改: ALLOWED_HOSTS = ['xxx.site.com']
    '''
    settings_path = source_folder + '/codelieche/settings.py'
    # 修改debug为False
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    # 设置允许的域名
    sed(settings_path,
        'ALLOWED_HOSTS = .+$',

        'ALLOWED_HOSTS =["%s, www.%s"]' % (site_name, site_name)
       )
    # 如果'secrret_key.py' 文件不存在，则创建密匙文件
    secret_key_file = source_folder + '/codelieche/secret_key.py'
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, "SECRET_KEY = '%s'" % key)
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')

def _update_virtualenv(source_folder):
    '''
    更新服务器，python虚拟环境，安装新的依赖包
    '''
    virtualenv_folder = source_folder + '/../virtualenv'
    if not exists(virtualenv_folder + '/bin/python'):
        run('virtualenv --python=python3 %s' % virtualenv_folder)

    run('%s/bin/pip install -r %s/requirements.txt' %(
        virtualenv_folder, source_folder
    ))

def _update_static_files(source_folder):
    '''更新静态文件'''
    run('cd %s && ../virtualenv/bin/python3 '\
      'manage.py collectstatic --noinput' % source_folder)

def _update_database(source_folder):
    '''更新数据库文件'''
    mysql_db_name = _inpute_value("请输入网站使用的数据库名:")
    mysql_user = _inpute_value("请输入mysql数据库用户名:")
    mysql_password = _inpute_value("请输入mysql数据库密码:")
    export_cmd = "export MYSQL_DB_NAME=%s MYSQL_USER=%s MYSQL_PASSWORD=%s" % (
        mysql_db_name, mysql_user, mysql_password
    )
    print(export_cmd)
    run('cd %s && %s && ../virtualenv/bin/python3 '\
    'manage.py migrate --noinput' % (source_folder, export_cmd))

def _inpute_value(notes):
    '''用户输入信息'''
    result = ''
    try:
        result = raw_input(notes)
    except Exception:
        result = input(notes)
    return result
