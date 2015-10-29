from base import Setting, SettingSet
from django.utils.translation import ugettext_lazy as _

SOCIAL_SET = SettingSet('social', _('Social settings'), _("Various setting related to site integreation with social services."), 100)

FACEBOOK_FANPAGE = Setting('FACEBOOK_FANPAGE', '', SOCIAL_SET, dict(
label = _("Facebook fanpage address"),
help_text = _("Adress of Facebook fanpage"),
required=False))

TWITTER_ADDRESS = Setting('TWITTER_ADDRESS', '', SOCIAL_SET, dict(
label = _("Twitter account"),
help_text = _("Adress of Twitter account"),
required=False))

GOOGLE_PLUS_FANPAGE = Setting('GOOGLE_PLUS_FANPAGE', '', SOCIAL_SET, dict(
label = _("Google+ fanpage address"),
help_text = _("Adress of Google+ fanpage"),
required=False))
