# resume_analyzer/settings.py

from pathlib import Path

# ------------------------------
# BASE DIRECTORY
# ------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ------------------------------
# SECURITY
# ------------------------------
SECRET_KEY = 'your-secret-key-here'  # Replace with your own
DEBUG = True
ALLOWED_HOSTS = []

# ------------------------------
# INSTALLED APPS
# ------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'analyzer',  # your app
]

# ------------------------------
# MIDDLEWARE
# ------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ------------------------------
# ROOT URLS
# ------------------------------
ROOT_URLCONF = 'resume_analyzer.urls'

# ------------------------------
# TEMPLATES
# ------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Optional global templates folder
        'APP_DIRS': True,  # Important! Looks inside app/templates/
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

# ------------------------------
# WSGI
# ------------------------------
WSGI_APPLICATION = 'resume_analyzer.wsgi.application'

# ------------------------------
# DATABASE
# ------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ------------------------------
# PASSWORD VALIDATION
# ------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# ------------------------------
# INTERNATIONALIZATION
# ------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# ------------------------------
# STATIC FILES
# ------------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# ------------------------------
# MEDIA FILES (uploads)
# ------------------------------
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ------------------------------
# DEFAULT PRIMARY KEY FIELD
# ------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
