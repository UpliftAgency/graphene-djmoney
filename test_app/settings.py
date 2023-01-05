import os

DEBUG = True

ROOT_URLCONF = "test_app.urls"

AUTH_USER_MODEL = "test_app.User"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

SECRET_KEY = "foobar"  # nosec

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "graphene_djmoney",
        "USER": "postgres",
        "PASSWORD": os.environ.get("PG_PASSWORD", ""),
        "HOST": "127.0.0.1",
        "PORT": "5432",
    }
}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "graphene_djmoney",
    "test_app",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

GRAPHENE = {
    "SCHEMA": "test_app.schema.schema",  # Where your Graphene schema lives
    "TESTING_ENDPOINT": "/graphql/",
    "MIDDLEWARE": [
        "middleware.CustomDjangoDebugMiddleware",
    ],
}

# Currencies & Money
BASE_CURRENCY = "USD"
CURRENCY_MAX_DIGITS = 10
CURRENCY_DECIMAL_PLACES = 2
