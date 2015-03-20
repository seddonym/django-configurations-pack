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

    @classmethod
    def setup(cls):
        super(AllowedHostsMixin, cls).setup()
        cls.ALLOWED_HOSTS = cls.get_allowed_hosts()

    @classmethod
    def get_allowed_hosts(cls):
        return [cls.get_setting('DOMAIN'), 'django-dbbackup']


class LoggingMixin(object):
    """Configuration mixin for setting the logging.
    
    Usage:
    
        LOG_PATH: required.
    """

    @classmethod
    def setup(cls):
        super(LoggingMixin, cls).setup()

        cls.LOGGING['handlers']['error']['filename'] = cls.get_error_log_file()
        cls.LOGGING['handlers']['debug']['filename'] = cls.get_debug_log_file()

        # Make sure we don't bother to mail admins if debug is True
        if cls.DEBUG:
            try:
                cls.LOGGING['loggers']['django.request']\
                                            ['handlers'].remove('mail_admins')
            except (KeyError, ValueError):
                pass

    @classmethod
    def get_error_log_file(cls):
        return os.path.join(cls.get_setting('LOG_PATH'), 'error.log')

    @classmethod
    def get_debug_log_file(cls):
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

        cls.DATABASES['default']['NAME'] = cls.get_default_database_name()
        cls.DATABASES['default']['USER'] = cls.get_default_database_user()
        cls.DATABASES['default']['PASSWORD'] = cls.get_setting(
                                                'DEFAULT_DATABASE_PASSWORD')

    @classmethod
    def get_default_database_name(cls):
        return cls.get_setting('PROJECT_NAME')

    @classmethod
    def get_default_database_user(cls):
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

        cls.STATIC_ROOT = cls.get_static_root()
        cls.MEDIA_ROOT = cls.get_media_root()
        cls.TEMPLATE_DIRS = cls.get_template_dirs()

    @classmethod
    def get_static_root(cls):
        return os.path.join(cls.get_setting('PROJECT_ROOT'), 'static')

    @classmethod
    def get_media_root(cls):
        return os.path.join(cls.get_setting('PROJECT_ROOT'), 'uploads')

    @classmethod
    def get_template_dirs(cls):
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
