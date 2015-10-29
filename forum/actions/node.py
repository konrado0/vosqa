from django.utils.html import strip_tags
from django.utils.translation import ugettext as _
from forum.models.action import ActionProxy
from forum.models import Comment, Question, Answer, NodeRevision
from forum.models import Image
from forum import settings, REQUEST_HOLDER
from lxml.html.clean import Cleaner, autolink_html, fromstring
from lxml import etree
from xml.sax.saxutils import unescape
from django.contrib import messages
from django.conf import settings as djsettings
import re
from copy import deepcopy
import urllib2
from django.core.files import File
from django.core.exceptions import ValidationError
from cStringIO import StringIO
import logging

logger = logging.getLogger(__name__)

autolink_reg = re.compile('<a\s((?![^>]*\starget=)[^>]*)>', re.IGNORECASE)
def autolink(html):
    if html:
        return autolink_reg.sub(r'<a \1 target="_blank">',autolink_html(html))
    return html

match_color = re.compile('(color:\s*[#\w]+;)', re.IGNORECASE)
def filter_style(doc):
    for e in etree.XPath("descendant-or-self::*[@style]")(doc):
#         print etree.tostring(e)         
        match = match_color.search(e.get("style"))
        if match:
#             print match.group()
            e.set("style", match.group())
        else:
            del e.attrib['style']
#         print etree.tostring(e)
    return doc

def get_html_cleaner():
    safeattrs = set(Cleaner.safe_attrs)
    safeattrs.add('frameborder')
    safeattrs.add('allowfullscreen')
    safeattrs.add('style')
    return Cleaner(embedded=False, safe_attrs = frozenset(safeattrs))

html_cleaner = get_html_cleaner()

_referers = (None,
    "https://www.google.com/search?q=fashion&hl=en&biw=939&bih=706&site=imghp&tbm=isch&source=lnms&sa=X&ei=WU5LVOC6N6XPygOatILAAg&ved=0CAgQ_AUoAQ&dpr=1.25",)

def download_image_file(url):
    inStream = None
    for referer in _referers:
        try:
            opener = urllib2.build_opener(urllib2.HTTPRedirectHandler(), urllib2.HTTPCookieProcessor())
            headers = [('User-agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:28.0) Gecko/20100101 Firefox/28.0'),]
            if referer:
                headers.append(('Referer', referer))
            opener.addheaders = headers
            inStream = opener.open(url)
            break
        except urllib2.HTTPError, e:
            logger.error(u'Unable to download image from url %s error "%s", code %d' % (url, e.reason, e.code))                
        except urllib2.URLError as e:
            logger.error(u'Unable to download image from url "%s" error %s' % (url, e.reason))
        inStream = None

    if not inStream:
        raise ValidationError(_(u"Unfortunatelly we are unable to dowload file from url '%s'. Please download it to your disk and try uploading it from disk.") % url)
    content_type = inStream.info().getheader('Content-Type')
    if not content_type or not content_type.lower().startswith("image"):
        logger.error(u'Url "%s" does not point to an image' % url)
        raise ValidationError(_(u"Url '%s' does not point to an image.") % url)

    file_name = url.rsplit('/', 1)[1].lower()
    ext = None
    if file_name.find('.') > 0:
        file_name, ext = file_name.rsplit('.', 1)
        if len(ext) > 4:
            if ext.find('?') > 2:
                ext = ext.split('?', 1)[0]
            else:
                ext = ext[:4]
    
    if ext not in djsettings.ALLOW_FILE_TYPES:
        ext = content_type.rsplit('/', 1)[1].lower()
        if ext not in djsettings.ALLOW_FILE_TYPES:
            raise ValidationError(u'Image type of "%s" is unsupported' % url)

    file_name = u"%s.%s" % (file_name, ext)
    img_temp = StringIO()
    size = 0
    while True:
        s = inStream.read(djsettings.ALLOW_MAX_FILE_SIZE / 8)
        if not s:
            break
        img_temp.write(s)
        size += len(s)
        if size >= djsettings.ALLOW_MAX_FILE_SIZE:
            logger.error(u'Specified image is too large - url "%s" error %s' % url)
            raise ValidationError(_(u"Image specified at url '%s' is too large") % url)

    img_temp.seek(0) 
    file_object = File(img_temp, file_name)
    file_object.size = size
    return file_object
    
def surround_img_with_link(el, url=None):
    e = etree.Element('a')
    e.set(u"href", url.replace(u"%", u"%%") if url else el.get("src"))
    e.set(u"class", u"clb")
    e.set(u"rel", u"noreferrer")
    e.tail = el.tail
    el.tail = None
    e.append(deepcopy(el))
    el.getparent().replace(el, e)
    
def template_url(url):
    if url.find(u"%"):
        url = url.replace(u"%", u"%%")
    return url.replace(djsettings.MEDIA_URL, ur"%(MEDIA_URL)s", 1)

class NodeEditAction(ActionProxy):
    image_id_prefix = "node_img"
    
    def __init__(self, *args, **kwargs):
        super(NodeEditAction, self).__init__(*args, **kwargs)
        self.new_images = []
        self.existing_images = []
    
    def create_revision_data(self, initial=False, **data):
        revision_data = dict(summary=data.get('summary', (initial and _('Initial revision') or '')), 
                             body=self.process_node_body(data['text']))        
        
        if data.get('title', None):
            revision_data['title'] = strip_tags(data['title'].strip())

        if data.get('tags', None):
            revision_data['tagnames'] = data['tags'].strip()
            
        if data.get('image', None):
            revision_data['main_image'] = data['image']
            
        return revision_data
    
    def post_save_processing(self):
        for image in self.new_images:
            image.nodes.add(self.node)
            image.save()
        
        for image in self.existing_images:
            if not self.node.image_set.filter(id=image.id).exists():
                image.nodes.add(self.node)
                image.save()
    
    def set_image_attributes(self, el, image):
        el.set(u"src", template_url(image.image.url))
        el.set(u"id", u"%s%d" % (self.image_id_prefix, image.id))
        el.set(u"style", u"display:block;")
        if image.width:
            el.set(u"width", unicode(image.width))
        if image.height:
            el.set(u"height", unicode(image.height))
        if el.getparent().tag != u"a":
            surround_img_with_link(el, image.upload_url)
    
    def process_node_body(self, html):
        try:
            html = autolink(html_cleaner.clean_html(html))
            
            #To stay on the safe side escape all % characters
            html = html.replace(u"%", u"%%")
            doc = filter_style(fromstring(html))
            
            for el in doc.iter(u'img'):
                src = el.get(u"src").replace(u"%%", u"%")
                if not src:
                    el.getparent().remove(el)
                
                if src.startswith(djsettings.APP_URL):
                    src.replace(djsettings.APP_URL, u"/", 1)
                
                if src.startswith(djsettings.MEDIA_URL):                
                    elem_id = el.get(u"id")
                    try:
                        if elem_id and elem_id.startswith(self.image_id_prefix):                        
                            image_id = int(elem_id.replace(self.image_id_prefix, ""))
                            image = Image.objects.get(id=image_id)
                            self.existing_images.append(image)
                            self.set_image_attributes(el, image)                        
                            continue
                    except:
                        logger.error(u'Malformed id (%s)found on our own img url %s' % (elem_id, src))
                    
                    try:
                        image = Image.objects.get(image=src.replace(djsettings.MEDIA_URL,u""))
                        self.set_image_attributes(el, image)
                        self.existing_images.append(image)                    
                        continue
                    except:
                        logger.error(u'Unable to locate img stored under url %s in Image table' % src)
                        if src.startswith(u"/"):
                            src = src.replace(u"/", djsettings.APP_URL, 1)         
    
                image_file = download_image_file(src)
                image = Image(image=image_file, upload_url=src)
                image.save()
                self.new_images.append(image)
                self.set_image_attributes(el, image)
            
            return etree.tounicode(doc, method="html")
        except ValidationError:
            for image in self.new_images:
                image.delete()
            raise
        except Exception:
            logger.exception(u'Unhandled exception while parsing "%s" body' % html)
            for image in self.new_images:
                image.delete()
            raise ValidationError(_(u"Unexpected error happened :("))

class AskAction(NodeEditAction):
    verb = _("asked")

    def process_data(self, **data):
        processed_data = self.create_revision_data(True, **data)
        if 'added_at' in data:
            processed_data['added_at'] = data['added_at']

        question = Question(author=self.user, **processed_data)
        question.save()
        self.node = question

        messages.info(REQUEST_HOLDER.request, self.describe(self.user))

    def describe(self, viewer=None):
        return _("%(user)s asked %(question)s") % {
            'user': self.hyperlink(self.user.get_profile_url(), self.friendly_username(viewer, self.user)),
            'question': self.hyperlink(self.node.get_absolute_url(), self.node.title)
        }

class AnswerAction(NodeEditAction):
    verb = _("answered")

    def process_data(self, **data):
        answer = Answer(author=self.user, parent=data['question'], **self.create_revision_data(True, **data))
        answer.save()
        self.node = answer

    def process_action(self):
        self.node.question.reset_answer_count_cache()

        messages.info(REQUEST_HOLDER.request, self.describe(self.user))


    def describe(self, viewer=None):
        question = self.node.parent
        return _("%(user)s answered %(asker)s on %(question)s") % {
            'user': self.hyperlink(self.user.get_profile_url(), self.friendly_username(viewer, self.user)),
            'asker': self.hyperlink(question.author.get_profile_url(), self.friendly_username(viewer, question.author)),
            'question': self.hyperlink(self.node.get_absolute_url(), question.title)
        }

class CommentAction(ActionProxy):
    verb = _("commented")

    def process_data(self, text='', parent=None):
        comment = Comment(author=self.user, parent=parent, body=autolink(strip_tags(text)))
        comment.save()
        self.node = comment

    def describe(self, viewer=None):
        return _("%(user)s commented on %(post_desc)s") % {
            'user': self.hyperlink(self.node.author.get_profile_url(), self.friendly_username(viewer, self.node.author)),
            'post_desc': self.describe_node(viewer, self.node.parent)
        }

class ReviseAction(NodeEditAction):
    verb = _("edited")

    def process_data(self, **data):
        revision_data = self.create_revision_data(**data)
        revision = self.node.create_revision(self.user, **revision_data)
        self.extra = revision.revision

    def process_action(self):
        self.node.last_edited = self
        self.node.save()

    def describe(self, viewer=None):
        return _("%(user)s edited %(post_desc)s") % {
            'user': self.hyperlink(self.user.get_profile_url(), self.friendly_username(viewer, self.user)),
            'post_desc': self.describe_node(viewer, self.node)
        }

    def get_absolute_url(self):
        return self.node.get_revisions_url()

class RetagAction(ActionProxy):
    verb = _("retagged")

    def process_data(self, tagnames=''):
        active = self.node.active_revision
        revision_data = dict(summary=_('Retag'), title=active.title, tagnames=strip_tags(tagnames.strip()), body=active.body)
        revision = self.node.create_revision(self.user, **revision_data)
        self.extra = revision.revision

    def process_action(self):
        self.node.last_edited = self
        self.node.save()

    def describe(self, viewer=None):
        return _("%(user)s retagged %(post_desc)s") % {
            'user': self.hyperlink(self.user.get_profile_url(), self.friendly_username(viewer, self.user)),
            'post_desc': self.describe_node(viewer, self.node)
        }

    def get_absolute_url(self):
        return self.node.get_revisions_url()

class RollbackAction(ActionProxy):
    verb = _("reverted")

    def process_data(self, activate=None):
        previous = self.node.active_revision
        self.node.activate_revision(self.user, activate)
        self.extra = "%d:%d" % (previous.revision, activate.revision)

    def process_action(self):
        self.node.last_edited = self
        self.node.save()

    def describe(self, viewer=None):
        revisions = [NodeRevision.objects.get(node=self.node, revision=int(n)) for n in self.extra.split(':')]

        return _("%(user)s reverted %(post_desc)s from revision %(initial)d (%(initial_sum)s) to revision %(final)d (%(final_sum)s)") % {
            'user': self.hyperlink(self.user.get_profile_url(), self.friendly_username(viewer, self.user)),
            'post_desc': self.describe_node(viewer, self.node),
            'initial': revisions[0].revision, 'initial_sum': revisions[0].summary,
            'final': revisions[1].revision, 'final_sum': revisions[1].summary,
        }

    def get_absolute_url(self):
        return self.node.get_revisions_url()

class CloseAction(ActionProxy):
    verb = _("closed")

    def process_action(self):
        self.node.marked = True
        self.node.nstate.closed = self
        self.node.last_edited = self
        self.node.update_last_activity(self.user, save=True)

    def cancel_action(self):
        self.node.marked = False
        self.node.nstate.closed = None
        self.node.update_last_activity(self.user, save=True)

    def describe(self, viewer=None):
        return _("%(user)s closed %(post_desc)s: %(reason)s") % {
            'user': self.hyperlink(self.user.get_profile_url(), self.friendly_username(viewer, self.user)),
            'post_desc': self.describe_node(viewer, self.node),
            'reason': self.extra
        }

class AnswerToCommentAction(ActionProxy):
    verb = _("converted")

    def process_data(self, new_parent=None):
        self.node.parent = new_parent
        self.node.node_type = "comment"

        for comment in self.node.comments.all():
            comment.parent = new_parent
            comment.save()

        self.node.body = autolink(strip_tags(self.node.body).replace(u"&nbsp;", " "))
        self.node.last_edited = self
        self.node.update_last_activity(self.user, save=True)
        try:
            self.node.abs_parent.reset_answer_count_cache()
        except AttributeError:
            pass

    def describe(self, viewer=None):
        return _("%(user)s converted an answer to %(question)s into a comment") % {
            'user': self.hyperlink(self.user.get_profile_url(), self.friendly_username(viewer, self.user)),
            'question': self.describe_node(viewer, self.node.abs_parent),
        }

class CommentToAnswerAction(ActionProxy):
    verb = _("converted")

    def process_data(self, question):
        self.node.parent = question
        self.node.node_type = "answer"
        self.node.last_edited = self
        self.node.update_last_activity(self.user, save=True)

        # Now updated the cached data
        question.reset_answer_count_cache()

    def describe(self, viewer=None):
        return _("%(user)s converted comment on %(question)s into an answer") % {
            'user': self.hyperlink(self.user.get_profile_url(), self.friendly_username(viewer, self.user)),
            'question': self.describe_node(viewer, self.node.abs_parent),
        }
class CommentToQuestionAction(NodeEditAction):
    verb = _("converted")

    def process_data(self, **data):
        revision_data = self.create_revision_data(**data)
        revision = self.node.create_revision(self.user, **revision_data)

        self.extra = {
            'covert_revision': revision.revision,
        }

        self.node.node_type = "question"
        self.node.parent = None
        self.node.abs_parent = None

    def process_action(self):
        self.node.last_edited = self
        self.node.save()

    def describe(self, viewer=None):
        return _("%(user)s converted comment on %(question)s to a new question") % {
            'user': self.hyperlink(self.user.get_profile_url(), self.friendly_username(viewer, self.user)),
            'question': self.describe_node(viewer, self.node.abs_parent),
        }

class AnswerToQuestionAction(NodeEditAction):
    verb = _("converted to question")

    def process_data(self,  **data):
        revision_data = self.create_revision_data(**data)
        revision = self.node.create_revision(self.user, **revision_data)

        original_question = self.node.question

        self.extra = {
            'covert_revision': revision.revision,
            'original_question': original_question
        }

        self.node.node_type = "question"
        self.node.parent = None
        self.node.abs_parent = None

        original_question.reset_answer_count_cache()

    def process_action(self):
        self.node.last_edited = self
        self.node.save()


    def describe(self, viewer=None):
        return _("%(user)s converted an answer to %(question)s into a separate question") % {
            'user': self.hyperlink(self.user.get_profile_url(), self.friendly_username(viewer, self.user)),
            'question': self.describe_node(viewer, self.node.abs_parent),
        }

class WikifyAction(ActionProxy):
    verb = _("wikified")

    def process_action(self):
        self.node.nstate.wiki = self
        self.node.last_edited = self
        self.node.update_last_activity(self.user, save=True)

    def cancel_action(self):
        self.node.nstate.wiki = None
        self.node.update_last_activity(self.user, save=True)

    def describe(self, viewer=None):
        return _("%(user)s marked %(node)s as community wiki.") % {
            'user': self.hyperlink(self.user.get_profile_url(), self.friendly_username(viewer, self.user)),
            'node': self.describe_node(viewer, self.node),
        }

