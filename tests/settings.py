import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = True

SECRET_KEY = 'is it secret, is is safe'

TIME_ZONE = 'Europe/Amsterdam'
USE_TZ = True

USE_I18N = True
USE_L10N = True

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',

    'helpers',
)

TEST_RUNNER = 'rainbowtests.test.runner.RainbowDiscoverRunner'

TEMPLATES = [{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3'
    }
}
LOCALE_PATHS = (
    os.path.join(os.path.dirname(BASE_DIR), 'helpers', 'locale'),
)
