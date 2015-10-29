import os.path

from base import Setting, SettingSet
from forms import ImageFormWidget

from django.utils.translation import ugettext_lazy as _
from django.forms.widgets import Textarea

BASIC_SET = SettingSet('basic', _('Basic settings'), _("The basic settings for your application"), 1)

APP_LOGO = Setting('APP_LOGO', '/upfiles/logo.png', BASIC_SET, dict(
label = _("Application logo"),
help_text = _("Your site main logo."),
widget=ImageFormWidget))

APP_LOGO_EMAIL = Setting('APP_LOGO_EMAIL', '/upfiles/logo.png', BASIC_SET, dict(
label = _("Logo for email"),
help_text = _("Logo used in email notifications."),
widget=ImageFormWidget))

APP_FAVICON = Setting('APP_FAVICON', '/m/default/media/images/favicon.ico', BASIC_SET, dict(
label = _("Favicon"),
help_text = _("Your site favicon."),
widget=ImageFormWidget))

APP_TITLE = Setting('APP_TITLE', u'VOSQA: Open Source Q&A Forum', BASIC_SET, dict(
label = _("Application title"),
help_text = _("The title of your application that will show in the browsers title bar")))

APP_SHORT_NAME = Setting(u'APP_SHORT_NAME', 'VOSQA', BASIC_SET, dict(
label = _("Application short name"),
help_text = "The short name for your application that will show up in many places."))

APP_KEYWORDS = Setting('APP_KEYWORDS', u'OSQA,CNPROG,forum,community', BASIC_SET, dict(
label = _("Application keywords"),
help_text = _("The meta keywords that will be available through the HTML meta tags.")))

APP_DESCRIPTION = Setting('APP_DESCRIPTION', u'Ask and answer questions.', BASIC_SET, dict(
label = _("Application description"),
help_text = _("The description of your application"),
widget=Textarea))

APP_COPYRIGHT = Setting('APP_COPYRIGHT', u'Copyright OSQA, 2010. Some rights reserved under creative commons license.', BASIC_SET, dict(
label = _("Copyright notice"),
help_text = _("The copyright notice visible at the footer of your page.")))

SUPPORT_URL = Setting('SUPPORT_URL', '', BASIC_SET, dict(
label = _("Support URL"),
help_text = _("The URL provided for users to get support. It can be http: or mailto: or whatever your preferred support scheme is."),
required=False))

CONTACT_URL = Setting('CONTACT_URL', '', BASIC_SET, dict(
label = _("Contact URL"),
help_text = _("The URL provided for users to contact you. It can be http: or mailto: or whatever your preferred contact scheme is."),
required=False))

LOAD_RESOURCES_FROM_CDN = Setting('LOAD_RESOURCES_FROM_CDN', True, BASIC_SET, dict(
label=_("Load JS/CSS resources from cdn"),
help_text = _("JS/CSS resources (jquery, tinymce etc) will be loaded from CDN instead of local."),
required=False,
))

EMBEDD_YOUTUBE_FROM_LINKS = Setting('EMBEDD_YOUTUBE_FROM_LINKS', True, BASIC_SET, dict(
label=_("Auto embed youtube videos"),
help_text = _("Try embedding youtube videos that are given as links."),
required=False,
))

EMBEDDED_VIDEO_WIDTH = Setting('EMBEDDED_VIDEO_WIDTH', 480, BASIC_SET, dict(
label = _("Embedded video width"),
help_text = _("Used for auto-embedded videos. Max 580 in current desing.")))

EMBEDDED_VIDEO_HEIGHT = Setting('EMBEDDED_VIDEO_HEIGHT', 360, BASIC_SET, dict(
label = _("Embedded video height"),
help_text = _("Used for auto-embedded videos.")))

EMBEDD_IMG_FROM_LINKS = Setting('EMBEDD_IMG_FROM_LINKS', True, BASIC_SET, dict(
label=_("Auto embed pictures"),
help_text = _("Try embedding pictures that are given as links.."),
required=False,
))

EMBEDDED_IMG_WIDTH = Setting('EMBEDDED_IMG_WIDTH', 480, BASIC_SET, dict(
label = _("Embedded pictures max width"),
help_text = _("Used for auto-embedded pictures. Max 580 in current desing.")))