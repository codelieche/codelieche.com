"""
Django settings for codelieche project.

Generated by 'django-admin startproject' using Django 2.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 把目录apps添加到path路径中，app都放在apps目录中
sys.path.append(os.path.join(BASE_DIR, "apps"))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'dxa&b2tew5g8$k10mqt$xm4(f$x80g@a8y+@w-!+zekv#as2cg'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# DEBUG = False

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 第三方app
    'rest_framework',
    'django_filters',
    'corsheaders',
    # 自己写的app
    'account',
    'modellog'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'codelieche.urls.main'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'codelieche.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.environ.get('MYSQL_DB_CODELIECHE', 'codelieche'),
        'USER': os.environ.get('MYSQL_USER', 'root'),
        'PASSWORD': os.environ.get('MYSQL_PASSWORD', ''),
        'HOST': os.environ.get('MYSQL_HOST', '127.0.0.1'),
        'PORT': os.environ.get('MYSQL_PORT', 3306)
    }
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
# 收集静态文件去STATIC_ROOT: python manage.py collectstatic
# STATIC_ROOT = os.path.join(os.path.join(BASE_DIR, '../static'))

# 开发环境使用SATICFILES_DIRS
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# 上传图片或者文件放在media中
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, '../media')

# 注册系统使用哪个用户模型
# 不需要加入中间的models
AUTH_USER_MODEL = 'account.UserProfile'
# 默认的登录地址: 当使用了login_required装饰器未传入login_url参数，默认会再settings中找LOGIN_URL
LOGIN_URL = '/account/login/'

# 使用自定义的后台auth认证方法
AUTHENTICATION_BACKENDS = (
    # 自定义的登录Backend
    'account.auth.CustomBackend',
)

# 设置session过期时间
SESSION_SAVE_EVERY_REQUEST = True
# 设置SESSION COOKIE过期时间 1h
SESSION_COOKIE_AGE = 60 * 60

# Django Rest Framework的配置
REST_FRAMEWORK = {
    # 设置分页
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        # 为了调试，需要BrowsableAPIRenderer,生产环境需要注释下面这行
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    # 设置DatetimeField字段的格式
    'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S',
    # 用户认证
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    )
}

# 跨域访问
CORS_ORIGIN_ALLOW_ALL = True
CORS_URLS_REGEX = r'^/api/.*$'
CORS_ALLOW_CREDENTIALS = True
