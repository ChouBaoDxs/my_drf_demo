"""
Django settings for my_drf_demo project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.index(os.path.join(BASE_DIR, 'apps'))
sys.path.index(os.path.join(BASE_DIR, 'extra_apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'kq%_m%w(#d5x5-t@3qm_8ohj*43plz9re$-gtpv5-acyj=x5++'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'drf_yasg',
    'django_filters',

    'user'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'my_drf_demo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'my_drf_demo.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

REST_FRAMEWORK = {
    'UNAUTHENTICATED_USER': None,
    'UNAUTHENTICATED_TOKEN': None,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # 'base.CustomAuthentication.CustomTokenAuthentication'
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        # 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
        # 'base.CustomPermissionCheck.CustomPermissionCheck'
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend', ],
    'DEFAULT_THROTTLE_CLASSES': [  # 访问频率限制配置
        # 'rest_framework.throttling.AnonRateThrottle',  # 匿名用户节流,通过IP地址判断
        # 'rest_framework.throttling.UserRateThrottle'  # 登录用户节流,通过token判断
        # 'base.CustomThrottle.LuffyAnonRateThrottle',
        # 'base.CustomThrottle.LuffyUserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        #     'anon': '2/m',  # 匿名用户对应的节流次数
        #     'user': '5/m'  # 登录用户对应 的节流次数
        'test_scope': '10/m',
        'luffy_anon': '10/m',
        'luffy_user': '20/m',
    },

    # url版本问题
    ## a. 基于url的get传参方式，如：/users?version=v1，url(r'^test/', TestView.as_view(),name='test'),
    ## b. 基于url的正则方式，如：/v1/users/，url(r'^(?P<version>[v1|v2]+)/test/', TestView.as_view(), name='test'),
    ## c. 基于 accept 请求头方式，如：Accept: application/json; version=1.0，url(r'^test/', TestView.as_view(), name='test'),
    ## d. 基于主机名方法，如：v1.example.com，url(r'^test/', TestView.as_view(), name='test'),
    ## e. 基于django路由系统的namespace，如：example.com/v1/users/
    ### urlpatterns = [
    ###     url(r'^v1/', ([
    ###                       url(r'test/', TestView.as_view(), name='test'),
    ###                   ], None, 'v1')),
    ###     url(r'^v2/', ([
    ###                       url(r'test/', TestView.as_view(), name='test'),
    ###                   ], None, 'v2')),
    ###
    ### ]

    'DEFAULT_VERSIONING_CLASS': "rest_framework.versioning.URLPathVersioning",
    'DEFAULT_VERSION': 'v1',  # 默认版本
    'ALLOWED_VERSIONS': ['v1', 'v2'],  # 允许的版本
    'VERSION_PARAM': 'version',  # URL中获取值的key

    # 解析器
    # 'DEFAULT_PARSER_CLASSES': [
    #     'rest_framework.parsers.JSONParser'
    #     'rest_framework.parsers.FormParser'
    # 'rest_framework.parsers.MultiPartParser'
    # ]

    # 渲染器
    'DEFAULT_RENDERER_CLASSES': (
        # 'rest_framework.renderers.JSONRenderer',  # 默认的是这个
        'my_drf_demo.renders.CodeMsgJsonRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    )
}

# 日志的配置信息
# if not DEBUG:
if DEBUG:
    import datetime

    LOG_DIR = os.path.join(BASE_DIR, 'logs')
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        # 日志格式
        'formatters': {
            'standard': {'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s]-[%(pathname)s] %(message)s'}
        },
        'filters': {

        },
        'handlers': {
            'default': {
                'level': 'INFO',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                # 'filename': os.path.join(LOG_DIR,
                #                          datetime.datetime.now().strftime("%Y-%m-%d  %H-%M-%S") + "default_handler.log"),
                'filename': os.path.join(LOG_DIR, "default_handler.log"),
                'backupCount': 20,
                # 'maxBytes': 1024 * 1024 * 5,  # 5 MB
                'when': 'D',
                'formatter': 'standard',
                'encoding': 'utf8',
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'standard',
            },
        },
        'loggers': {
            'default': {
                'handlers': ['default', 'console'],
                'level': 'INFO',
                'propagate': False
            },
            'django': {
                'handlers': ['default', 'console'],
                'level': 'INFO',
                'propagate': False,
            },
        },
    }
