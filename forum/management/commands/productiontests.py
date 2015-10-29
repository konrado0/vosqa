from django.core.management.base import NoArgsCommand
import unittest
import traceback

from forum.models import User, Question, Comment, QuestionSubscription, SubscriptionSettings, Answer, Node, NodeRevision
from forum.utils.mail import send_template_email
from forum.utils.html import html2text

class Command(NoArgsCommand):
    help = """
    If you need Arguments, please check other modules in 
    django/core/management/commands.
    """

    def handle_noargs(self, **options):
        suite = unittest.TestLoader().loadTestsFromTestCase(AnswerNotificationTest)
        unittest.TextTestRunner().run(suite)

class AnswerNotificationTest(unittest.TestCase):


    def testRenderOfNotificationEmail(self):
        for node in Node.objects.all():
            node.body = node.body.replace(u"%", u"%%")
            node.save()
        
        for revision in NodeRevision.objects.all():
            revision.body = revision.body.replace(u"%", u"%%")
            revision.save()
#         for q in Question.objects.all():
#             for answer in q.answers.all():
#                 try:
#                     s = unicode(answer.html)
# #                     s = answer.html.decode('utf-8', 'strict')
#                 except Exception, e:                                        
#                     print traceback.format_exc()                    
#                     self.assertFalse(True, "Exception during string decoding:\n%s \nExeption: \n %s" % (answer.html, e))
#                 try:
#                     print html2text(answer.html)                    
# #                     send_template_email([u'conrado_o@tlen.pl'], "notifications/newanswer.html", {'answer': answer})
#                 except Exception, e:                                        
#                     print traceback.format_exc()
#                     self.assertFalse(True, "Exception has been thrown while rendering email for answer:\n%s \nExeption: \n %s" % (answer.html, e))
