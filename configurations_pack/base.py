"""Base settings shared by all environments.
This is a reusable basic settings file.
"""
from configurations import Configuration
from . import mixins


class BaseConfiguration(Configuration):
    """Base configuration, intended for use with the configuration mixins.
    Implements a helpful method get_setting() for getting settings
    that we are not sure have been set.
    
    Usage:
    
        class MyConfiguration(BaseConfiguration):
    
            @classmethod
            def setup(cls):
                super(MyConfiguration, cls).setup()
                cls.FOO = cls.get_setting('BAR')
                
    """
    @classmethod
    def get_setting(cls, name):
        "Shortcut for attempting to get a particular setting on the class."
        try:
            return getattr(cls, name)
        except AttributeError:
            raise ValueError('You must define a %s setting.' % name)


class StandardConfiguration(mixins.UnifiedDebugMixin,
                        mixins.SecretSettingsMixin,
                        mixins.LoggingMixin,
                        mixins.DatabaseMixin,
                        mixins.StaticMediaAndTemplatesMixin,
                        BaseConfiguration):
    """A configuration that collects together lots of standard
    configuration patterns for use across projects."""

    TIME_ZONE = 'GB'
    USE_TZ = True
    USE_I18N = True
    USE_L10N = True
    LANGUAGE_CODE = 'en-GB'
    LANGUAGES = (
        ('en-GB', 'British English'),
    )

    SITE_ID = 1
    LOGIN_URL = '/login/'
    LOGOUT_URL = '/logout/'
    LOGIN_REDIRECT_URL = '/'

    STATIC_URL = '/static/'
    MEDIA_URL = '/uploads/'

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
        }
    }

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
                'datefmt' : "%d/%b/%Y %H:%M:%S"
            },
        },
        'handlers': {
            'error': {
                'level':'ERROR',
                'class':'logging.handlers.RotatingFileHandler',
                'filename': '/var/log/django/buzzhire/error.log',  # - filled in by LoggingMixin
                'maxBytes': 50000,
                'backupCount': 2,
                'formatter': 'standard',
            },
            'debug': {
                'level':'DEBUG',
                'class':'logging.handlers.RotatingFileHandler',
                'filename': '/var/log/django/buzzhire/debug.log',  # filled in by LoggingMixin
                'maxBytes': 50000,
                'backupCount': 2,
                'formatter': 'standard',
            },
            'mail_admins': {
                'level': 'ERROR',
                'class': 'django.utils.log.AdminEmailHandler',
                'include_html': True,
            },
        },
        'loggers': {
            'django': {
                'handlers':['error'],
                'propagate': True,
                'level':'DEBUG',
            },
            'django.request': {
                'handlers': ['mail_admins', 'error'],
                'level': 'ERROR',
                'propagate': False,
            },
            'project': {
                'handlers':['debug'],
                'propagate': True,
                'level':'DEBUG',
            },
        }
    }

    TEMPLATE_CONTEXT_PROCESSORS = Configuration.TEMPLATE_CONTEXT_PROCESSORS + (
        'django.core.context_processors.request',
    )

    ROOT_URLCONF = 'urls'

    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.admin',
    )

    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )
