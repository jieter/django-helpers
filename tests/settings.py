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
    },]
