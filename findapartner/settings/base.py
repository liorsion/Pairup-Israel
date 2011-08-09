from unipath import FSPath as Path

PROJECT_DIR = Path(__file__).absolute().ancestor(2)

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('Lior Sion', 'lior.sion@gmail.com'),
)

MANAGERS = ADMINS

AUTH_PROFILE_MODULE='userprofile.UserProfile'

TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True

SEND_BROKEN_LINK_EMAILS = True

ACCOUNT_ACTIVATION_DAYS = 7

AUTO_GENERATE_AVATAR_SIZES = 80
AVATAR_STORAGE_DIR = "avatars"

AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend',
                           'social_auth.backends.twitter.TwitterBackend',
                            'social_auth.backends.facebook.FacebookBackend',
                            'social_auth.backends.google.GoogleOAuthBackend',
                            'social_auth.backends.google.GoogleOAuth2Backend',
                            'social_auth.backends.google.GoogleBackend',
                            'social_auth.backends.yahoo.YahooBackend',
                            'social_auth.backends.contrib.linkedin.LinkedinBackend',
                            'findapartner.utils.backends.EmailUserBackend',
                            'findapartner.utils.backends.CaseInsensitiveModelBackend',)

TEMPLATE_CONTEXT_PROCESSORS = ("django.contrib.auth.context_processors.auth",
                                "django.core.context_processors.debug",
                                "django.core.context_processors.i18n",
                                "django.core.context_processors.media",
                                "django.core.context_processors.static",
                                "django.contrib.messages.context_processors.messages",
                                "findapartner.utils.context_processors.social_context")

MEDIA_ROOT = PROJECT_DIR.parent.child('data')
MEDIA_URL = '/media/'

STATIC_ROOT = PROJECT_DIR.parent.child('static_root')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    str(PROJECT_DIR.child('static')),
)
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

SECRET_KEY = 'c120v)_7u%=(nfn*bjpswynqbr_l(1q28t=0x#&1ed*m@gqhd1'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware'
)

SESSION_ENGINE =  'django.contrib.sessions.backends.cached_db'

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    PROJECT_DIR.child('templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'south',
    'sentry',
    'avatar',
    'sentry.plugins.sentry_urls',
    'sentry.client',
    'social_auth',
    'epio_commands',
    'registration',
    'django_extensions',
    'categories',
    'experience_categories',
    'ideas',
    'partner',
    'userprofile',
    'django.contrib.admin',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

TWITTER_CONSUMER_KEY         = 'iNaPL7Ep9KolWivSFkJGw'
TWITTER_CONSUMER_SECRET      = 't9fbVEvkPaNGEyqbRQecEkkGRcPkWGFuFVl2u7hZ88'
FACEBOOK_APP_ID              = '142972025779422'
FACEBOOK_API_SECRET          = 'c89c93bbed6787913ee60c79dcffa60f'
LINKEDIN_CONSUMER_KEY        = 'HrlawIAeCvjWEsZXI-xu3nmasw9tufCbowSZJCay-oRAehckzOk6gPM6Lwtflq02'
LINKEDIN_CONSUMER_SECRET     = 'rFFkK9jgtwrLQicLMqmGA6v79XvwRldFbnjqaVQavyWnmOZ-PUtT6sds1Szv86GB'
ORKUT_CONSUMER_KEY           = ''
ORKUT_CONSUMER_SECRET        = ''
GOOGLE_CONSUMER_KEY          = ''
GOOGLE_CONSUMER_SECRET       = ''
GOOGLE_OAUTH2_CLIENT_KEY     = ''
GOOGLE_OAUTH2_CLIENT_SECRET  = ''
FOURSQUARE_CONSUMER_KEY      = ''
FOURSQUARE_CONSUMER_SECRET   = ''

FACEBOOK_EXTENDED_PERMISSIONS = "email, publish_stream"
FACEBOOK_FIELD_SELECTORS = ['link',]   
FACEBOOK_EXTRA_DATA = [('link', 'public_profile_url'),]

TWITTER_FIELD_SELECTORS = ['profile_image_url', 'url']   
TWITTER_EXTRA_DATA = [('profile_image_url', 'profile_image_url'),
                      ('url', 'public_profile_url')]
LINKEDIN_EXTRA_FIELD_SELECTORS  = ['summary', 'specialties', 'skills', 'picture-url', 'public-profile-url']
LINKEDIN_EXTRA_DATA = [('summary', 'summary'),
                       ('specialties', 'specialties'),
                       ('skills', 'skills'),
                       ('picture-url', 'picture_url'),
                       ('public-profile-url', 'public_profile_url')]
                                  

LOGIN_URL          = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGIN_ERROR_URL    = '/accounts/login-error/'
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/profile/edit/'
SOCIAL_AUTH_NEW_ASSOCIATION_REDIRECT_URL = '/profile/edit/'
SOCIAL_AUTH_DISCONNECT_REDIRECT_URL = '/profile/edit/'
SOCIAL_AUTH_ERROR_KEY = 'social_errors'

SOCIAL_AUTH_COMPLETE_URL_NAME  = 'socialauth_complete'
SOCIAL_AUTH_ASSOCIATE_URL_NAME = 'socialauth_associate_complete'

from django.template.defaultfilters import slugify
SOCIAL_AUTH_USERNAME_FIXER = lambda u: slugify(u)
SOCIAL_AUTH_UUID_LENGTH = 16
SOCIAL_AUTH_EXPIRATION = 'expires'
SOCIAL_AUTH_ASSOCIATE_BY_MAIL = True

