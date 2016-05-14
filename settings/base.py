import json
import os

from django.core.exceptions import ImproperlyConfigured

# Fetch JSON data for settings stored outside version control
with open('settings/secret_settings.json') as json_file:
    secrets_data = json.loads(json_file.read())


# Function to fetch secret settings
def get_secret_setting(setting, data=secrets_data):
    try:
        return secrets_data[setting]
    except KeyError:
        raise ImproperlyConfigured(setting + ' setting not found.')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

SECRET_KEY = get_secret_setting('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = []

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'FEC_Toolbox.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'FEC_Toolbox.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
STATIC_URL = '/static/'

# FEC_Toolbox Settings: Directories
# ---------------------------------
# Base directory setting used to create default settings for other directories (e.g., REPORT_DIR, BULK_LOAD_DIR).
BASE_FEC_DIR = 'C:/data/fec'

# Parent directory used to house all downloaded reports. Default is: <BASE_FEC_DIR>/reports
REPORTS_DIR = BASE_FEC_DIR + '/reports'

# Test directory used to download data during testing.
TEST_DIR = BASE_FEC_DIR + '/test'

# FEC_Toolbox Settings: Downloads
# -------------------------------
# To avoid hardcoding file formats, use this dictionary to specify a user-defined key for each possible report type.
# Values for each key are dictionaries of other settings, such as delimiter, url pattern, file extension and
# save path.
FILE_TYPES = {'pdf': {'file_extension': '.pdf',
                      'delimiter': None,
                      'electronic_url_pattern': None,
                      'paper_url_pattern': None,
                      'a_tag_id': None,
                      'json_tag': 'pdf_url',
                      'save_path': REPORTS_DIR + '/pdf/'},
              'csv': {'file_extension': '.csv',
                      'delimiter': ',',
                      # This elec_url_pattern works only for reports at least 1000 lines long.
                      'electronic_url_pattern': 'http://docquery.fec.gov/comma/<report_id>.fec',
                      'paper_url_pattern': 'http://docquery.fec.gov/paper/fecpprcsv/<report_id>.fec',
                      'a_tag_id': 'csvfile',
                      'json_tag': None,
                      'save_path': REPORTS_DIR + '/text/csv/'},
              'ascii28': {'file_extension': '.txt',
                          'delimiter': chr(28),
                          'electronic_url_pattern': 'http://docquery.fec.gov/dcdev/posted/<report_id>.fec',
                          'paper_url_pattern': 'http://docquery.fec.gov/paper/posted/<report_id>.fec',
                          'a_tag_id': 'asciifile',
                          'json_tag': None,
                          'save_path': REPORTS_DIR + '/text/ascii28/'}
              }

# ---------------
# OLD SETTINGS:
# ---------------
"""

# Default filetypes to download upon base Report class instantiation
# DOWN_NOW = ['ascii28']
DOWN_NOW = {'ascii28': {}}

# Notes only below this point:
# ----------------------------

# Default delimiter for text data. Default is: chr(28)
# DEFAULT_DELIM = chr(28)

# Specifies in base Report class whether the indicated format should be downloaded and retained in memory upon
# instantiation.
# MEM_LOAD = ('ascii28', FILE_TYPES)

# Specifies in base Report class whether the application should attempt to download a report in the specified format
# upon instantiation and load that data into the database. Set to None if the data should not be loaded automatically.
# If this value does not match a key in FILE_TYPES, you must override DB_LOAD_URL below.
# DB_LOAD_DELIM = 'ascii28'

# URL pattern that should be used to try to download a report with the delimiter specified in DB_LOAD_DELIM
# DB_LOAD_URL = None
# if DB_LOAD_DELIM in FILE_TYPES.keys():
#     DB_LOAD_URL = FILE_TYPES[DB_LOAD_DELIM]['url_pattern']

# List of URL modifiers for paper vs. electronically filed reports. Used by paper_or_plastic.
# URL_RPT_TYPE_MODS = ('', '')
# http://docquery.fec.gov/paper/fecpprcsv/1006117.fec
# http://docquery.fec.gov/paper/posted/1006117.fec
"""