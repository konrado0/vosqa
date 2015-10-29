# encoding:utf-8
import os.path
import sys
import logging

SITE_ID = 1

SECRET_KEY = 'a;::qCl1mfh?avagttOJ;8f5Rr54d,9qy7;o15M2cYO75?OQo51u3LnQ;!8N.:,7'

CACHE_MAX_KEY_LENGTH = 235

MIDDLEWARE_CLASSES = [
    'django.middleware.csrf.CsrfViewMiddleware',
    'forum.middleware.django_cookies.CookiePreHandlerMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.common.CommonMiddleware',
    'forum.middleware.extended_user.ExtendedUser',
    'forum.middleware.anon_user.ConnectToSessionMessagesMiddleware',
    'forum.middleware.request_utils.RequestUtils',
    'forum.middleware.cancel.CancelActionMiddleware',
    'forum.middleware.admin_messages.AdminMessagesMiddleware',
    'forum.middleware.custom_pages.CustomPagesFallbackMiddleware',
    'forum.middleware.django_cookies.CookiePostHandlerMiddleware',
]

TEMPLATE_CONTEXT_PROCESSORS = [
    'django.core.context_processors.request',
    'forum.context.application_settings',
    'django.contrib.messages.context_processors.messages',
    'forum.user_messages.context_processors.user_messages',
    'django.contrib.auth.context_processors.auth',
]

ROOT_URLCONF = 'urls'
APPEND_SLASH = True

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__),'forum','skins').replace('\\','/'),
)

#Redefine this if your account urls use diffrent protocol then rest of application
APP_AUTH_URL = None

# FILE_UPLOAD_TEMP_DIR = os.path.join(os.path.dirname(__file__), 'tmp').replace('\\','/')
FILE_UPLOAD_HANDLERS = ("django.core.files.uploadhandler.MemoryFileUploadHandler",
 "django.core.files.uploadhandler.TemporaryFileUploadHandler",)
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

# Absolute filesystem path to the directory that will hold user-uploaded files.
UPFILES_ALIAS = 'upfiles/'
MEDIA_ROOT = os.path.join(os.path.dirname(__file__),'forum',UPFILES_ALIAS)
MEDIA_URL = '/upfiles/'

STATIC_ROOT = os.path.join(os.path.dirname(__file__),'forum','static')
STATIC_URL = '/static/'

# Max size of uploaded images
DJANGORESIZED_DEFAULT_SIZE = [720, 720]

#Uploaded avatar imiges settings
AVATAR_UPLOADS_ALIAS = 'avatar/'
USER_AVATAR_SIZE = [128, 128]
AVATAR_FILL_COLOR = (220,220,220,0)

ALLOW_FILE_TYPES = ('jpg', 'jpeg', 'gif', 'bmp', 'png', 'tiff')
# Max size of images uploaded from url
ALLOW_MAX_FILE_SIZE = 1024 * 1024 * 3 +1

#  PAGINATION SETTINGS
DEFAULT_PAGESIZES = (12, 24, 36)
DEFAULT_PAGESIZE = 24
DEFAULT_FLOW_PAGESIZE = 15
DEFAULT_LIST_TEMPLATE = 'kafelki.html'
ALLOWED_LIST_TEMPLATES = ('kafelki.html', 'lista.html')
NEXT_PAGE_LOAD_TRIGGER = 300 # in pixels

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

#sorl-thumbnail loggin level sorl-thumbnail logging
logging.getLogger('sorl.thumbnail').setLevel(logging.ERROR)

# User settings
from settings_local import *

TINYMCE_CONFIG = ur"""
    menubar : false, statusbar : false, plugins: ["fullscreen, link, image, media, paste, textcolor, autoresize",],
    toolbar: "formatselect | bold italic underline forecolor | blockquote link image media | bullist numlist | undo redo | fullscreen",
    extended_valid_elements : "iframe[src|width|height|name|id|class|align|style|frameborder|border|allowtransparency|allowfullscreen]",
    entity_encoding: "raw",
    body_class: "answer-body",
    content_css : "/m/default/media/style/style.css",
    height : 250,
    block_formats: "Paragraph=p;Header 1=h2;Header 2=h3",
    image_dimensions: false,
    relative_urls : false,
    media_alt_source: false,
    media_poster: false,
    """

template_loaders = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'forum.modules.template_loader.module_templates_loader',
    'forum.skins.load_template_source',
)
TEMPLATE_LOADERS = list(template_loaders) if DEBUG else [ ('django.template.loaders.cached.Loader', template_loaders) ]

try:
    if len(FORUM_SCRIPT_ALIAS) > 0:
        APP_URL = '%s/%s' % (APP_URL, FORUM_SCRIPT_ALIAS[:-1])
except NameError:
    pass

if not APP_AUTH_URL:
    APP_AUTH_URL = APP_URL
app_url_split = APP_URL.split("://")

APP_PROTOCOL = app_url_split[0]
APP_DOMAIN = app_url_split[1].split('/')[0]
APP_BASE_URL = '%s://%s' % (APP_PROTOCOL, APP_DOMAIN)

FORCE_SCRIPT_NAME = ''

for path in app_url_split[1].split('/')[1:]:
    FORCE_SCRIPT_NAME = FORCE_SCRIPT_NAME + '/' + path

if FORCE_SCRIPT_NAME.endswith('/'):
    FORCE_SCRIPT_NAME = FORCE_SCRIPT_NAME[:-1]

#Module system initialization
MODULES_PACKAGE = 'forum_modules'
MODULES_FOLDER = os.path.join(SITE_SRC_ROOT, MODULES_PACKAGE)

MODULE_LIST = filter(lambda m: getattr(m, 'CAN_USE', True), [
        __import__('forum_modules.%s' % f, globals(), locals(), ['forum_modules'])
        for f in os.listdir(MODULES_FOLDER)
        if os.path.isdir(os.path.join(MODULES_FOLDER, f)) and
           os.path.exists(os.path.join(MODULES_FOLDER, "%s/__init__.py" % f)) and
           not f in DISABLED_MODULES
])

[MIDDLEWARE_CLASSES.extend(
        ["%s.%s" % (m.__name__, mc) for mc in getattr(m, 'MIDDLEWARE_CLASSES', [])]
                          ) for m in MODULE_LIST]

[TEMPLATE_LOADERS.extend(
        ["%s.%s" % (m.__name__, tl) for tl in getattr(m, 'TEMPLATE_LOADERS', [])]
                          ) for m in MODULE_LIST]


INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.humanize',
    'django.contrib.sitemaps',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'forum',
    'sorl.thumbnail',    
]

if DEBUG:
    try:
        import debug_toolbar
        MIDDLEWARE_CLASSES.append('debug_toolbar.middleware.DebugToolbarMiddleware')
        INSTALLED_APPS.append('debug_toolbar')        
    except:
        pass

if not DEBUG:
    try:
        import rosetta
        INSTALLED_APPS.append('rosetta')
    except:
        pass

AUTHENTICATION_BACKENDS = ['forum_modules.localauth.backends.EmailAuthBackend', 
                           'django.contrib.auth.backends.ModelBackend',]
