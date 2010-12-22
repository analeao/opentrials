# -*- encoding: utf-8 -*-

# OpenTrials: a clinical trials registration system
#
# Copyright (C) 2010 BIREME/PAHO/WHO, ICICT/Fiocruz e
#                    Ministério da Saúde do Brasil
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 2.1 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful, 
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import os
gettext = lambda s: s

DEBUG = False
TEMPLATE_DEBUG = DEBUG
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

ADMINS = (
    ('Luciano Ramalho', 'luciano.ramalho@bireme.org'),
    ('Fabio Montefuscolo', 'fabio.montefuscolo@bireme.org'),
    ('Rafael Soares', 'rafael.soares@bireme.org'),
)

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Brasilia'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'pt-BR'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"

MEDIA_ROOT = os.path.join(PROJECT_PATH, 'static')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/static/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '*06=j&&^n71^a&%%3rs%7lla+^(n^v1w@@dp_rxvi#&(xo7meq'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'middleware.scriptprefix.ScriptPrefixMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'middleware.user_locale.UserLocaleMiddleware',
    #'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'flatpages_polyglot.middleware.FlatPagePolyglotMiddleware',
)

ROOT_URLCONF = 'opentrials.urls'
LOGIN_REDIRECT_URL = '/accounts/dashboard/'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    
    os.path.join(PROJECT_PATH, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.flatpages',
    'django.contrib.markup',
    'deleting',
    'vocabulary',
    'repository',
    'reviewapp',
    'tickets',
    'assistance',
    'decsclient',
    'diagnostic',
    'polyglot',
    'registration',  # django-registration package
    'flatpages_polyglot',
    'south',
    'fossil',
)

TEMPLATE_CONTEXT_PROCESSORS =(
    'django.core.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.csrf',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'context_processors.opentrials.polyglot',
    'context_processors.opentrials.jquery',
    'context_processors.opentrials.google_analytics',
    'context_processors.opentrials.latest_tweets',
)

AUTH_PROFILE_MODULE = "reviewapp.UserProfile"

#################################################################
### BEGIN Clinical Trials Repository customization settings
###
### see also settings_local-SAMPLE.py for private customization settings.

# this id must match the record with the correct domain name in the
# django_site table; the initial values for that table are defined
# in opentrials/fixtures/initial_data.json
SITE_ID = 2 # change if necessary to match a record in django_site

SITE_TITLE = u'Registro Brasileiro de Ensaios Clínicos'
SEND_BROKEN_LINK_EMAILS = True
DECS_SERVICE = 'http://decs.bvs.br/cgi-bin/mx/cgi=@vmx/decs'

# Notes:
# 1) source: http://www.i18nguy.com/unicode/language-identifiers.html
# 2) the first managed language is considered the default and is
#    also the source language for content translation purposes
MANAGED_LANGUAGES_CHOICES = (
    (u'en', gettext(u'English')),
    (u'es', gettext(u'Español')),
    (u'pt-BR', gettext(u'Portuguese')),
)
TARGET_LANGUAGES = MANAGED_LANGUAGES_CHOICES[1:] # exlude source language
MANAGED_LANGUAGES = [code for code, label in MANAGED_LANGUAGES_CHOICES]
# TODO: implement this as default on new submission forms
#LANGUAGES = MANAGED_LANGUAGES_CHOICES
DEFAULT_SUBMISSION_LANGUAGE = u'en'

# django-registration: for how long the activation link is valid
ACCOUNT_ACTIVATION_DAYS = 7

# django-registration: set to False to suspend new user registrations
REGISTRATION_OPEN = True

ATTACHMENTS_PATH = 'attachments'
SUBMISSIONS_XML_PATH = 'submissions_xml'

# Name of Primary Registry
REG_NAME = 'REBEC'

FIXTURE_DIRS = ('fixtures',)

PAGINATOR_CT_PER_PAGE = 10

TWITTER = 'ensaiosclinicos'
TWITTER_TIMEOUT = 18000 # expires in 5 min

JQUERY_URL = 'http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js'
JQUERY_UI_URL = 'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.0/jquery-ui.min.js'

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = ['--with-coverage', '--with-doctest', '--doctest-tests', '--doctest-extension=txt'] # --doctest-fixtures, --with-profile
#NOSE_PLUGINS = []
SKIP_SOUTH_TESTS = True
SOUTH_TESTS_MIGRATE = False

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

FORMAT_MODULE_PATH = 'formats'

### END Clinical Trials Repository customization settings
#################################################################

# Deployment settings: there *must* be an unversioned settings_local.include
# file in the current directory. See sample file at settings_local-SAMPLE.include
# FIXME: why not use a simple "try: from settings_local import * except ImportError: pass" ?
execfile(os.path.join(PROJECT_PATH,'settings_local.include'))
