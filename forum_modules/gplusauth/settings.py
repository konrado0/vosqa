from forum.settings import EXT_KEYS_SET
from forum.settings.base import Setting
from django.utils.translation import ugettext_lazy as _

GOOGLE_CONSUMER_KEY = Setting('GOOGLE_CONSUMER_KEY', '', EXT_KEYS_SET, dict(
label = _("Google+ consumer key"),
help_text = _("""
Get this key at the <a href="https://console.developers.google.com/"> Google Developers Console</a> to enable
authentication in your site through Google+. More <a href="https://developers.google.com/+/web/signin/redirect-uri-flow">information</a>.
"""),
required=False))

GOOGLE_CONSUMER_SECRET = Setting('GOOGLE_CONSUMER_SECRET', '', EXT_KEYS_SET, dict(
label = _("Google+ consumer secret"),
help_text = _("""
This your Google+ consumer secret that you'll get in the same place as the consumer key.
"""),
required=False))
