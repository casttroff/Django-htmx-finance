from pathlib import Path
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-hfjjz86s+pz6y4p=&mxz)dis&l$+mt2)6r$ho@))^5))f#$whp"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.import_export",
    "modeltranslation",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    'django.contrib.sites',
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    
    # external apps
    "django_extensions",
    "debug_toolbar", # Debug Toolbar
    "widget_tweaks",
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'django_filters',
    'django_htmx',
    'template_partials',
    'crispy_forms',
    'crispy_tailwind',
    'import_export',    
    # project apps
    "tracker",
    
    
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"

CRISPY_TEMPLATE_PACK = "tailwind"

SITE_ID = 1

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware", # Debug Toolbar
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
]

ROOT_URLCONF = "finance_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "finance_project.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


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


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"
STATICFILES_DIRS = [
    BASE_DIR / 'static'
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]

AUTH_USER_MODEL = 'auth.User'
LOGIN_REDIRECT_URL = 'index'
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
PAGE_SIZE = 5
UNFOLD = {
    "SITE_TITLE": 'Admin',
    "SITE_HEADER": 'Administración',
    "EXTENSIONS": {
        "modeltranslation": {
            "flags": {
                "en": "🇬🇧",
                "fr": "🇫🇷",
                "nl": "🇧🇪",
            },
        },
    },
    # "SIDEBAR": {
    #         "show_search": False,  # Search in applications and models names
    #         "show_all_applications": False,  # Dropdown with all applications and models
    #         "navigation": [
    #             {
    #                 "title": _("Navegación"),
    #                 "separator": True,  # Top border
    #                 "collapsible": True,  # Collapsible group of links
    #                 "items": [
    #                     {
    #                         "title": _("Dashboard"),
    #                         "icon": "dashboard",  # Supported icon set: https://fonts.google.com/icons
    #                         "link": reverse_lazy("admin:index"),
    #                         "badge": "sample_app.badge_callback",
    #                         "permission": lambda request: request.user.is_superuser,
    #                     },
    #                     {
    #                         "title": _("Users"),
    #                         "icon": "people",
    #                         "link": reverse_lazy("admin:users_user_changelist"),
    #                     },
    #                 ],
    #             },
    #         ],
    #     },
    # "TABS": [
    #     {
    #         "models": [
    #             "app_label.model_name_in_lowercase",
    #         ],
    #         "items": [
    #             {
    #                 "title": "Your custom title",
                    
    #             },
    #         ],
    #     },
    # ],
    
}
LANGUAGES = (
    ('en', 'English'),
    ('de', 'German'),
    ('es', 'Spanish'),
)
MODELTRANSLATION_LANGUAGES = ('es', 'en', 'de')
MODELTRANSLATION_PREPOPULATE_LANGUAGE = 'es'
MODELTRANSLATION_FALLBACK_LANGUAGES = ('es', 'en')
def badge_callback(request):
    return 3
