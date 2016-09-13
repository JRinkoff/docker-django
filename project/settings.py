import os
from app.handler import skip_redis_connectionerror, skip_debug

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = False
ALLOWED_HOSTS = ['.{{project}}.com']
INTERNAL_IPS = ('127.0.0.1', )
PREPEND_WWW = True

SECRET_KEY = os.environ.get('SECRET_KEY', 'm+stn!t$67en7e&-1e2#&i29=@hv@4s7v)pbf&o5hwsd0gj439')

# Application definition
INSTALLED_APPS = (
    'cachalot',
    'compressor',
    'jet',
    'dbbackup',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'debug_toolbar',
    'template_timings_panel',

    'app',
)

MIDDLEWARE_CLASSES = (
    'app.middleware.cache.DisableClientSideCachingMiddleware',
    'django.middleware.gzip.GZipMiddleware',

    'htmlmin.middleware.HtmlMinifyMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',

    'htmlmin.middleware.MarkRequestMiddleware',
    'app.middleware.general.InternalUseOnlyMiddleware',
    'app.middleware.cache.TTLMiddleware',
    'app.middleware.cache.VaryMiddleware',
)

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    # 'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    'template_timings_panel.panels.TemplateTimings.TemplateTimings',
    # 'cachalot.panels.CachalotPanel',
]

ROOT_URLCONF = '{{project}}.urls'

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

WSGI_APPLICATION = '{{project}}.wsgi.application'

# Database
DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'HOST': 'postgres',
            'PORT': '5432',
            'NAME': 'django',
            'USER': 'django',
            'PASSWORD': 'django'
        }
}

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'unix:///app/docker/etc/redis.sock',
    },
    'cachalot': {  # Use separate cache for Cachalot
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'unix:///app/docker/etc/redis.sock',
        'KEY_PREFIX': 'cachalot',
    },
    'template_fragments': {
        'BACKEND': 'app.cache.filebased.SmartFileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'cache/template_fragments/'),
        'OPTIONS': {
            'MAX_ENTRIES': -1  # set max_entries to -1 to disable culling
        }
    },
}

CACHALOT_CACHE = 'cachalot'

# Internationalization
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

# Email settings
ADMINS = [('Admin', os.environ.get('EMAIL_HOST_USER', '')), ]
EMAIL_HOST = os.environ.get('EMAIL_HOST', '')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
EMAIL_USE_TLS = True
SERVER_EMAIL = os.environ.get('EMAIL_HOST_USER', '')
DEFAULT_FROM_EMAIL = os.environ.get('EMAIL_HOST_USER', '')

# Security
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = 'DENY'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'app.handler.ThrottledAdminEmailHandler',
            'filters': ['skip_debug', 'skip_redis_connectionerror'],
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
            },
        },
    'filters': {
            'skip_debug': {
                '()': 'django.utils.log.CallbackFilter',
                'callback': skip_debug,
            },
            'skip_redis_connectionerror': {
                '()': 'django.utils.log.CallbackFilter',
                'callback': skip_redis_connectionerror,
            }
    },
}

SILENCED_SYSTEM_CHECKS = ['cachalot.E001']

# Backup settings
DBBACKUP_HOSTNAME = ALLOWED_HOSTS[0]  # Needed for error reporting from dbbackup
DBBACKUP_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
DBBACKUP_STORAGE_OPTIONS = {
    'access_key': os.environ.get('AWS_ACCESS_KEY', ''),
    'secret_key': os.environ.get('AWS_SECRET_KEY', ''),
    'bucket_name': os.environ.get('AWS_BUCKET_NAME', ''),
}
