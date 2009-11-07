# Django settings for sequia project.

from local_settings import *

#LOGIN_REDIRECT_URL="/"
DEBUG = True
TEMPLATE_DEBUG = DEBUG
AUTH_PROFILE_MODULE = "profiles.UserProfile"
DEFAULT_CHARSET = 'utf-8'
MANAGERS = ADMINS
DATABASE_ENGINE = 'mysql'
SEARCH_ENGINE = 'mysql'
ACCOUNT_ACTIVATION_DAYS = 7
SITE_ID = 1
USE_I18N = True
ADMIN_MEDIA_PREFIX = '/media/admin/'
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)


MEDIA_ROOT = os.path.join(SITE_ROOT,'media')
MEDIA_URL = '/media'
TEMPLATE_DIRS = (
SITE_ROOT+"/templates",
)
ROOT_URLCONF = 'urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'lugar',
    'sequias',
)
