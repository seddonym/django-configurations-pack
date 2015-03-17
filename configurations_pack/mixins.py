import os
from .utils import settings_from_module, classproperty


class UnifiedDebugMixin(object):
    """Configuration mixin for making the thumbnail and template debug
    equal to the normal debug setting.
    """
    @classmethod
    def setup(cls):
        super(UnifiedDebugMixin, cls).setup()
        # Unify all debug settings
        cls.THUMBNAIL_DEBUG = cls.TEMPLATE_DEBUG = cls.DEBUG


class SecretSettingsMixin(object):
    """Configuration mixin for importing the settings from secret.py"""

    @classmethod
    def pre_setup(cls):
        super(SecretSettingsMixin, cls).pre_setup()

        # Set any settings from secret.py
        for name, value in settings_from_module('settings.secret').items():
            setattr(cls, name, value)


class AllowedHostsMixin(object):
    """Configuration mixin for setting ALLOWED_HOSTS.
    
    Usage:
    
        DOMAIN: required.
    """

    @classproperty
    def ALLOWED_HOSTS(cls):
        return [cls.get_setting('DOMAIN'), 'django-dbbackup']


class LoggingMixin(object):
    """Configuration mixin for setting the logging.
    
    Usage:
    
        LOG_PATH: required.
    """

    @classmethod
    def setup(cls):
        super(LoggingMixin, cls).setup()

        cls.LOGGING['handlers']['error']['filename'] = cls.ERROR_LOG_FILE
        cls.LOGGING['handlers']['debug']['filename'] = cls.DEBUG_LOG_FILE

        # Make sure we don't bother to mail admins if debug is True
        if cls.DEBUG:
            try:
                cls.LOGGING['loggers']['django.request']\
                                            ['handlers'].remove('mail_admins')
            except (KeyError, ValueError):
                pass

    @classproperty
    def ERROR_LOG_FILE(cls):
        return os.path.join(cls.get_setting('LOG_PATH'), 'error.log')

    @classproperty
    def DEBUG_LOG_FILE(cls):
        return os.path.join(cls.get_setting('LOG_PATH'), 'debug.log')


class DatabaseMixin(object):
    """Configuration mixin for setting the databases.
    
    Usage:
    
        PROJECT_NAME: setting for the user and database name
        DEFAULT_DATABASE_PASSWORD: setting for the database password; should
                                   be defined in secret.py.
    """

    @classmethod
    def post_setup(cls):
        super(DatabaseMixin, cls).post_setup()

        cls.DATABASES['default']['NAME'] = cls.DEFAULT_DATABASE_NAME
        cls.DATABASES['default']['USER'] = cls.DEFAULT_DATABASE_USER
        cls.DATABASES['default']['PASSWORD'] = cls.get_setting(
                                                'DEFAULT_DATABASE_PASSWORD')

    @classproperty
    def DEFAULT_DATABASE_NAME(cls):
        return cls.get_setting('PROJECT_NAME')

    @classproperty
    def DEFAULT_DATABASE_USER(cls):
        return cls.get_setting('PROJECT_NAME')



class StaticMediaAndTemplatesMixin(object):
    """Configuration mixin for setting the path to the static, media
    and template directories.
    
    Usage:
    
        PROJECT_ROOT: Required.
    """

    @classmethod
    def setup(cls):
        super(StaticMediaAndTemplatesMixin, cls).setup()
        cls.MEDIA_ROOT = cls.get_media_root()
        cls.TEMPLATE_DIRS = cls.get_template_dirs()

    @classproperty
    def STATIC_ROOT(cls):
        return os.path.join(cls.get_setting('PROJECT_ROOT'), 'static')

    @classproperty
    def MEDIA_ROOT(cls):
        return os.path.join(cls.get_setting('PROJECT_ROOT'), 'uploads')

    @classproperty
    def TEMPLATE_DIRS(cls):
        TEMPLATE_DIR = os.path.join(cls.get_setting('PROJECT_ROOT'),
                                    'templates')
        return (TEMPLATE_DIR,)



# class EmailMixin(object):
#     """Configuration mixin for setting the email.
#
#     Usage:
#
#         EMAIL_HOST: required
#     """
#
#     @classmethod
#     def setup(cls):
#         super(EmailMixin, cls).setup()
#
#
#         self._settings['EMAIL_HOST_USER'] = self.get_email_host_user()
#         self._settings['SERVER_EMAIL'] = self.get_server_email()
#         self._settings['DEFAULT_FROM_EMAIL'] = self.get_default_from_email()
#
#     @classmethod
#     def get_email_host_user(cls):
#         return cls.get_setting('')
