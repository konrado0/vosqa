import re
from datetime import date
from django import forms
from forum.models import *
from django.utils.translation import ugettext as _
from django.conf import settings as django_settings
from django.core.exceptions import ValidationError

from django.utils.encoding import smart_unicode
from general import NextUrlField, UserNameField
from django.utils.safestring import mark_safe

from forum import settings, REQUEST_HOLDER
from forum.actions.node import download_image_file

from forum.modules import call_all_handlers

import logging
from forum.models.resized_image_field import ResizableImageField

logger = logging.getLogger(__name__)

class TitleField(forms.CharField):
    def __init__(self, *args, **kwargs):
        super(TitleField, self).__init__(*args, **kwargs)

        self.required = True
        self.max_length = 255
        self.widget = forms.TextInput(attrs={'size' : 70, 'autocomplete' : 'off', 'maxlength' : self.max_length})
        self.label  = _('title')
        self.help_text = _('please enter a descriptive title for your question')
        self.initial = ''

    def clean(self, value):
        super(TitleField, self).clean(value)

        if len(value) < settings.FORM_MIN_QUESTION_TITLE:
            raise forms.ValidationError(_('title must be must be at least %s characters') % settings.FORM_MIN_QUESTION_TITLE)

        return value

class EditorField(forms.CharField):
    def __init__(self, *args, **kwargs):
        super(EditorField, self).__init__(*args, **kwargs)

        self.widget = forms.Textarea(attrs={'id':'editor'})
        self.label  = _('content')
        self.help_text = u''
        self.initial = ''


class QuestionEditorField(EditorField):
    def __init__(self, *args, **kwargs):
        super(QuestionEditorField, self).__init__(*args, **kwargs)
        self.required = not bool(settings.FORM_EMPTY_QUESTION_BODY)


    def clean(self, value):
        super(QuestionEditorField, self).clean(value)

        if not bool(settings.FORM_EMPTY_QUESTION_BODY) and (len(re.sub('[ ]{2,}', ' ', value)) < settings.FORM_MIN_QUESTION_BODY):
            raise forms.ValidationError(_('question content must be at least %s characters') % settings.FORM_MIN_QUESTION_BODY)

        return value

class AnswerEditorField(EditorField):
    def __init__(self, *args, **kwargs):
        super(AnswerEditorField, self).__init__(*args, **kwargs)
        self.required = True

    def clean(self, value):
        super(AnswerEditorField, self).clean(value)

        if len(re.sub('[ ]{2,}', ' ', value)) < settings.FORM_MIN_QUESTION_BODY:
            raise forms.ValidationError(_('answer content must be at least %s characters') % settings.FORM_MIN_QUESTION_BODY)

        return value


class TagNamesField(forms.CharField):
    def __init__(self, user=None, *args, **kwargs):
        super(TagNamesField, self).__init__(*args, **kwargs)

        self.required = True
        self.widget = forms.TextInput(attrs={'size' : 50, 'autocomplete' : 'off'})
        self.max_length = 100
        self.label  = _('tags')
        #self.help_text = _('please use space to separate tags (this enables autocomplete feature)')
        self.help_text = mark_safe(_("""Tags are short keywords, with no spaces within. At least %(min)s and up to %(max)s tags can be used.
         <br>Order of tags is important. Put those, that describe your question best, first.""") % {
            'min': settings.FORM_MIN_NUMBER_OF_TAGS, 'max': settings.FORM_MAX_NUMBER_OF_TAGS    
        })
        self.initial = ''
        self.user = user

    def clean(self, value):
        super(TagNamesField, self).clean(value)

        value = super(TagNamesField, self).clean(value)
        data = value.strip().lower().replace(u'#', u'')

        split_re = re.compile(r'[ ,]+')
        taglist = split_re.split(data)        

        if len(taglist) > settings.FORM_MAX_NUMBER_OF_TAGS or len(taglist) < settings.FORM_MIN_NUMBER_OF_TAGS:
            raise forms.ValidationError(_('please use between %(min)s and %(max)s tags') % { 'min': settings.FORM_MIN_NUMBER_OF_TAGS, 'max': settings.FORM_MAX_NUMBER_OF_TAGS})

        list_temp = []
        tagname_re = re.compile(r'^[\w+#\.-]+$', re.UNICODE)
        for tag in taglist:
            if len(tag) > settings.FORM_MAX_LENGTH_OF_TAG or len(tag) < settings.FORM_MIN_LENGTH_OF_TAG:
                raise forms.ValidationError(_('please use between %(min)s and %(max)s characters in you tags') % { 'min': settings.FORM_MIN_LENGTH_OF_TAG, 'max': settings.FORM_MAX_LENGTH_OF_TAG})
            if not tagname_re.match(tag):
                raise forms.ValidationError(_('please use following characters in tags: letters , numbers, and characters \'.#-_\''))
            # only keep one same tag
            if tag not in list_temp and len(tag.strip()) > 0:
                list_temp.append(tag)

        if settings.LIMIT_TAG_CREATION and not self.user.can_create_tags():
            existent = Tag.objects.filter(name__in=list_temp).values_list('name', flat=True)

            if len(existent) < len(list_temp):
                unexistent = [n for n in list_temp if not n in existent]
                raise forms.ValidationError(_("You don't have enough reputation to create new tags. The following tags do not exist yet: %s") %
                        ', '.join(unexistent))

        return u' '.join(list_temp)

class WikiField(forms.BooleanField):
    def __init__(self, disabled=False, *args, **kwargs):
        super(WikiField, self).__init__(*args, **kwargs)
        self.required = False
        self.label  = _('community wiki')
        self.help_text = _('if you choose community wiki option, the question and answer do not generate points and name of author will not be shown')
        if disabled:
            self.widget=forms.CheckboxInput(attrs={'disabled': "disabled"})
    def clean(self,value):
        return value

class EmailNotifyField(forms.BooleanField):
    def __init__(self, *args, **kwargs):
        super(EmailNotifyField, self).__init__(*args, **kwargs)
        self.required = False
        self.widget.attrs['class'] = 'nomargin'

class SummaryField(forms.CharField):
    def __init__(self, *args, **kwargs):
        super(SummaryField, self).__init__(*args, **kwargs)
        self.required = False
        self.widget = forms.TextInput(attrs={'size' : 50, 'autocomplete' : 'off'})
        self.max_length = 300
        self.label  = _('update summary:')
        self.help_text = _('enter a brief summary of your revision (e.g. fixed spelling, grammar, improved style, this field is optional)')


class FeedbackForm(forms.Form):
    message = forms.CharField(label=_('Your message:'), max_length=800,widget=forms.Textarea(attrs={'cols':60}))
    next = NextUrlField()

    def __init__(self, user, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        if not user.is_authenticated():
            self.fields['name'] = forms.CharField(label=_('Your name:'), required=False)
            self.fields['email'] = forms.EmailField(label=_('Email (not shared with anyone):'), required=True)

        # Create anti spam fields
        spam_fields = call_all_handlers('create_anti_spam_field')
        if spam_fields:
            spam_fields = dict(spam_fields)
            for name, field in spam_fields.items():
                self.fields[name] = field

            self._anti_spam_fields = spam_fields.keys()
        else:
            self._anti_spam_fields = []

import urllib2
from django.core.files import File
from cStringIO import StringIO
from django.conf import settings as djsettings
from forum.models.resized_image_field import ResizableImageFieldFile

class UrlOrUploadImageWidget(forms.Widget):
    """
    A Widget that enables image upload either by supplying url or standard upload from disk.
    """
    
    needs_multipart_form = True
    upload_name = "%s_upload"
    url_name = "%s_url"
    
    def __init__(self, attrs=None, required=True,  image=None):
        # years is an optional list/tuple of years to use in the "year" select box.
        self.attrs = attrs or {}
        self.required = required

    def render(self, name, value, attrs=None):        
        image = ""
        
        if isinstance(value, ResizableImageFieldFile):
            image = '<li>Current image:<div><img src="%s" /></div></li>' % value.url
            value = (None, None)        
        elif not value:
            value = (None, None)
        
        upload = forms.ClearableFileInput(attrs=dict(self.attrs, accept='image/*'))
        urlinput = forms.TextInput(attrs=self.attrs)
        
        return mark_safe(
                """
                <ul class="imageUpload" >                
                <li>Specify image url: %s</li>
                <li>Or upload image file from disk: %s</li>%s
                </ul>
                """ % (urlinput.render(self.url_name % name, value[1], attrs),
                       upload.render(self.upload_name % name, value[0], attrs),
                       image 
                       ))        
        

    def value_from_datadict(self, data, files, name):
        upload = forms.ClearableFileInput()
        file_object = upload.value_from_datadict(data, files, self.upload_name % name)
        
        urlinput = forms.TextInput()
        url = urlinput.value_from_datadict(data, files, self.url_name % name)
        
        return (file_object, url)

class UrlOrUploadImageField(forms.ImageField):
    """
    Extension of forms.ImageField allowing upload by just by specifying url.
    """
    
    widget = UrlOrUploadImageWidget(attrs={'class':'image_widget_group'})
    default_error_messages = {
        'invalid_image': _(u"Upload a valid image. The file you uploaded or one pointed by the url was either not an image or a corrupted image."),
#         'url_not_image': _(u"File in specified url does not match accepted image format."),
#         'file_too_large': _(u"Upload a valid image. File in specified url is too large."),
#         'download_failed': _(u"Unfortunatelly we are unable to dowload file from url You specified. Please download it to your disk and try uploading it using 'Choose file' button."),
    }
    
    def __init__(self, *args, **kwargs):
        super(UrlOrUploadImageField, self).__init__(*args, **kwargs)
        self.url = None
    
    def get_url(self):
        return self.url
    
    def to_python(self, data):
        if data[0]:
            return super(UrlOrUploadImageField, self).to_python(data[0])
        
        if not data[1]:
            return None
        
        try:
            self.url = data[1]
        
#             opener = urllib2.build_opener(urllib2.HTTPRedirectHandler(), urllib2.HTTPCookieProcessor())
#             opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:28.0) Gecko/20100101 Firefox/28.0')]
#             inStream = opener.open(url)
#             
#             content_type = inStream.info().getheader('Content-Type')
#             if not content_type or not content_type.lower().startswith("image"):
#                 logger.error(u'Url %s does not point to image' % url)
#                 raise ValidationError(self.error_messages['url_not_image'])
#             
#             file_name = url.rsplit('/', 1)[1]
#             ext = file_name.rsplit('.', 1)[1].lower()
#             if ext not in djsettings.ALLOW_FILE_TYPES:
#                 ext = content_type.rsplit('/', 1)[1].lower()
#                 if ext not in djsettings.ALLOW_FILE_TYPES:  
#                     raise ValidationError(self.error_messages['url_not_image'])
#                 file_name = "file.%s" % ext
# 
#             img_temp = StringIO()
#             size = 0
#             while True:
#                 s = inStream.read(djsettings.ALLOW_MAX_FILE_SIZE / 8)
#                 if not s:
#                     break
#                 img_temp.write(s)
#                 size += len(s)
#                 if size >= djsettings.ALLOW_MAX_FILE_SIZE:
#                     raise ValidationError(self.error_messages['file_too_large'])
#             
#             img_temp.seek(0)
#             file_object = File(img_temp, file_name)
#             file_object.size = size
            file_object = download_image_file(self.url)
            return super(UrlOrUploadImageField, self).to_python(file_object)
        except ValidationError:
            raise
#         except urllib2.URLError as e:
#             logger.error('Unable to download image from url %s error %s, code %d' % (url, str(e), e.code))
#             raise ValidationError(str(self.error_messages['download_failed']))        
        except:
            raise ValidationError(self.error_messages['invalid_image'])        
    

class AskForm(forms.Form):
    title  = TitleField()
    text   = QuestionEditorField()
    image  = UrlOrUploadImageField(label=_(u"Choose image describing what you want to find"))
    
    def __init__(self, data=None, files=None, user=None, *args, **kwargs):
        super(AskForm, self).__init__(data, files, *args, **kwargs)

        self.fields['tags']   = TagNamesField(user)
        
#         if not user.is_authenticated() or (int(user.reputation) < settings.CAPTCHA_IF_REP_LESS_THAN and not (user.is_superuser or user.is_staff)):
#             spam_fields = call_all_handlers('create_anti_spam_field')
#             if spam_fields:
#                 spam_fields = dict(spam_fields)
#                 for name, field in spam_fields.items():
#                     self.fields[name] = field
# 
#                 self._anti_spam_fields = spam_fields.keys()
#             else:
#                 self._anti_spam_fields = []

#         if settings.WIKI_ON:
#             self.fields['wiki'] = WikiField()

class AnswerForm(forms.Form):
    text   = AnswerEditorField()
    wiki   = WikiField()

    def __init__(self, data=None, user=None, *args, **kwargs):
        super(AnswerForm, self).__init__(data, *args, **kwargs)
        
#         if not user.is_authenticated() or (int(user.reputation) < settings.CAPTCHA_IF_REP_LESS_THAN and not (user.is_superuser or user.is_staff)):
#             spam_fields = call_all_handlers('create_anti_spam_field')
#             if spam_fields:
#                 spam_fields = dict(spam_fields)
#                 for name, field in spam_fields.items():
#                     self.fields[name] = field
# 
#                 self._anti_spam_fields = spam_fields.keys()
#             else:
#                 self._anti_spam_fields = []

#         if settings.WIKI_ON:
#             self.fields['wiki'] = WikiField()

class RetagQuestionForm(forms.Form):
    tags   = TagNamesField()
    # initialize the default values
    def __init__(self, question, *args, **kwargs):
        super(RetagQuestionForm, self).__init__(*args, **kwargs)
        self.fields['tags'].initial = question.tagnames

class RevisionForm(forms.Form):
    """
    Lists revisions of a Question or Answer
    """
    revision = forms.ChoiceField(widget=forms.Select(attrs={'style' : 'width:520px'}))

    def __init__(self, post, *args, **kwargs):
        super(RevisionForm, self).__init__(*args, **kwargs)

        revisions = post.revisions.all().values_list('revision', 'author__username', 'revised_at', 'summary').order_by('-revised_at')

        date_format = '%c'
        self.fields['revision'].choices = [
            (r[0], u'%s - %s (%s) %s' % (r[0], smart_unicode(r[1]), r[2].strftime(date_format), r[3]))
            for r in revisions]

        self.fields['revision'].initial = post.active_revision.revision

class EditQuestionForm(forms.Form):
    title  = TitleField()
    text   = QuestionEditorField()
    summary = SummaryField()
    image = UrlOrUploadImageField(label=_(u"Choose image if you want to change it"), required=False)

    def __init__(self, question, user, revision=None, files=None, *args, **kwargs):
        super(EditQuestionForm, self).__init__(files=files, *args, **kwargs)

        if revision is None:
            revision = question.active_revision

        self.fields['title'].initial = revision.title
        self.fields['text'].initial = revision.html
        self.fields['image'].initial = revision.main_image.image

        self.fields['tags'] = TagNamesField(user)
        self.fields['tags'].initial = revision.tagnames

#         if not user.is_authenticated() or (int(user.reputation) < settings.CAPTCHA_IF_REP_LESS_THAN and not (user.is_superuser or user.is_staff)):
#             spam_fields = call_all_handlers('create_anti_spam_field')
#             if spam_fields:
#                 spam_fields = dict(spam_fields)
#                 for name, field in spam_fields.items():
#                     self.fields[name] = field
# 
#                 self._anti_spam_fields = spam_fields.keys()
#             else:
#                 self._anti_spam_fields = []

#         if settings.WIKI_ON:
#             self.fields['wiki'] = WikiField(disabled=(question.nis.wiki and not user.can_cancel_wiki(question)), initial=question.nis.wiki)

class EditAnswerForm(forms.Form):
    text = AnswerEditorField()
    summary = SummaryField()

    def __init__(self, answer, user, revision=None, *args, **kwargs):
        super(EditAnswerForm, self).__init__(*args, **kwargs)

        if revision is None:
            revision = answer.active_revision

        self.fields['text'].initial = revision.html

#         if not user.is_authenticated() or (int(user.reputation) < settings.CAPTCHA_IF_REP_LESS_THAN and not (user.is_superuser or user.is_staff)):
#             spam_fields = call_all_handlers('create_anti_spam_field')
#             if spam_fields:
#                 spam_fields = dict(spam_fields)
#                 for name, field in spam_fields.items():
#                     self.fields[name] = field
# 
#                 self._anti_spam_fields = spam_fields.keys()
#             else:
#                 self._anti_spam_fields = []
        
#         if settings.WIKI_ON:
#             self.fields['wiki'] = WikiField(disabled=(answer.nis.wiki and not user.can_cancel_wiki(answer)), initial=answer.nis.wiki)

class EditUserForm(forms.Form):
    email = forms.EmailField(label=u'Email', help_text=_('this email does not have to be linked to gravatar'), required=True, max_length=75, widget=forms.TextInput(attrs={'size' : 35}))
    avatar = forms.ImageField(label=_("Avatar image"), help_text=_('Use only if you want to change avatar. Image should be %sx%s but will be resized if it is not.' % (
            django_settings.USER_AVATAR_SIZE[0], django_settings.USER_AVATAR_SIZE[1])), required=False, )
    realname = forms.CharField(label=_('Real name'), required=False, max_length=255, widget=forms.TextInput(attrs={'size' : 35}))
    website = forms.URLField(label=_('Website'), required=False, max_length=255, widget=forms.TextInput(attrs={'size' : 35}))
    city = forms.CharField(label=_('Location'), required=False, max_length=255, widget=forms.TextInput(attrs={'size' : 35}))
    birthday = forms.DateField(label=_('Date of birth'), help_text=_('will not be shown, used to calculate age, format: YYYY-MM-DD'), required=False, widget=forms.TextInput(attrs={'size' : 35}))
    about = forms.CharField(label=_('Profile'), required=False, widget=forms.Textarea(attrs={'cols' : 60}))

    def __init__(self, user, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)
        if settings.EDITABLE_SCREEN_NAME or (REQUEST_HOLDER.request.user.is_authenticated() and REQUEST_HOLDER.request.user.is_superuser):
            self.fields['username'] = UserNameField(label=_('Screen name'))
            self.fields['username'].initial = user.username
            self.fields['username'].user_instance = user
        self.fields['email'].initial = user.email
        self.fields['realname'].initial = user.real_name
        self.fields['website'].initial = user.website
        self.fields['city'].initial = user.location

        if user.date_of_birth is not None:
            self.fields['birthday'].initial = user.date_of_birth

        self.fields['about'].initial = user.about
        self.user = user

    def clean_email(self):
        if self.user.email != self.cleaned_data['email']:
            if settings.EMAIL_UNIQUE:
                if 'email' in self.cleaned_data:
                    from forum.models import User
                    try:
                        User.objects.get(email = self.cleaned_data['email'])
                    except User.DoesNotExist:
                        return self.cleaned_data['email']
                    except User.MultipleObjectsReturned:
                        logging.error("Found multiple users sharing the same email: %s" % self.cleaned_data['email'])
                        
                    raise forms.ValidationError(_('this email has already been registered, please use another one'))
        return self.cleaned_data['email']
        

NOTIFICATION_CHOICES = (
    ('i', _('Instantly')),
    #('d', _('Daily')),
    #('w', _('Weekly')),
    ('n', _('No notifications')),
)

class SubscriptionSettingsForm(forms.ModelForm):
    enable_notifications = forms.BooleanField(widget=forms.HiddenInput, required=False)
    member_joins = forms.ChoiceField(widget=forms.RadioSelect, choices=NOTIFICATION_CHOICES)
    new_question = forms.ChoiceField(widget=forms.RadioSelect, choices=NOTIFICATION_CHOICES)
    new_question_watched_tags = forms.ChoiceField(widget=forms.RadioSelect, choices=NOTIFICATION_CHOICES)
    subscribed_questions = forms.ChoiceField(widget=forms.RadioSelect, choices=NOTIFICATION_CHOICES)

    class Meta:
        model = SubscriptionSettings
        fields = ['enable_notifications', 'member_joins', 'new_question', 'new_question_watched_tags', 'subscribed_questions']

class UserPreferencesForm(forms.Form):
    sticky_sorts = forms.BooleanField(required=False, initial=False)



