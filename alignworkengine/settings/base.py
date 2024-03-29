import os
import secrets
from datetime import timedelta
from pathlib import Path

import dj_database_url
from decouple import config
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = config("SECRET_KEY")

# Application definition
DEFAULT_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "corsheaders",
    "channels",
    "django_countries",
    "django_extensions",
    "django_filters",
    "django_rest_passwordreset",
    "drf_yasg",
    "drf_spectacular",
    "rest_framework",
    "rest_framework_simplejwt",
    "storages",
]

LOCAL_APPS = [
    # auth apps
    "accounts",
    # chat apps
    "assistant",
    "documents",
    "agreements",
    "meetings",
    "updates",
    "notifications",
    "analytics",
    "projects",
    # payment apps
    # "payment",
]

OTHER_APPS = [
    # "debug_toolbar",
]

INSTALLED_APPS = DEFAULT_APPS + LOCAL_APPS + THIRD_PARTY_APPS + OTHER_APPS


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",  # Custom added
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "alignworkengine.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "alignworkengine.wsgi.application"


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ================================ CUSTOM CONFIGS =======================================
AUTH_USER_MODEL = "accounts.User"
ASGI_APPLICATION = "alignworkengine.asgi.application"

LOGIN_URL = "login"
LOGOUT_URL = "logout"
LOGIN_REDIRECT_URL = "index"  # "dashboard"
LOGOUT_REDIRECT_URL = "login"


def get_origin_list(env_variable, default=""):
    origins = config(env_variable, default)
    return [origin.strip() for origin in origins.split(",") if origin.strip()]


# ==> CORS
CORS_ALLOWED_ORIGINS = get_origin_list("CORS_ORIGINS")
CORS_ALLOWED_CREDENTIALS = True
# CORS_ALLOW_ALL_ORIGINS = True

# ==> CSRF
CSRF_TRUSTED_ORIGINS = get_origin_list("CSRF_TRUSTED_ORIGINS")

# ==> CONSTANTS
CART_SESSION_ID = secrets.token_urlsafe(16)

# ==> AUTHENTICATION
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

# ==> REST FRAMEWORK
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=10),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "AlignWork API",
    "DESCRIPTION": "AlignWork description",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": True,
}

# ================================ CUSTOM CONFIGS =======================================

# ================================ CUSTOM VARIABLES =======================================
# ==> OPENAI
OPENAI_API_KEY = config("OPENAI_API_KEY")
ASSISTANT_ID = config("ASSISTANT_ID")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# ==> ZOOM
ZOOM_ACCOUNT_ID = config("ZOOM_ACCOUNT_ID")
ZOOM_CLIENT_ID = config("ZOOM_CLIENT_ID")
ZOOM_CLIENT_SECRET = config("ZOOM_CLIENT_SECRET")

# ==> GOOGLE CALENDAR
GOOGLE_NOTIFICATION_WEBHOOK_URL = config("GOOGLE_NOTIFICATION_WEBHOOK_URL")

GOOGLE_OAUTH2_CLIENT_SECRETS_JSON = "keys/gauth/secrets/cal_api_client_secret.json"
GOOGLE_OAUTH2_SCOPES = [
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/calendar.events",
    "https://www.googleapis.com/auth/calendar.events.readonly",
]
GOOGLE_OAUTH2_REDIRECT_URI = "http://localhost:8000/oauth2callback"
# ================================ CUSTOM VARIABLES =======================================


# ================================ DJANGO COUNTRIES CUSTOM CONFIG FOR DJANGO 5x =======================================
# from django_countries.widgets import LazyChoicesMixin

# LazyChoicesMixin.get_choices = lambda self: self._choices
# LazyChoicesMixin.choices = property(
#     LazyChoicesMixin.get_choices, LazyChoicesMixin.set_choices
# )

# ================================ DJANGO COUNTRIES CUSTOM CONFIG FOR DJANGO 5x =======================================
