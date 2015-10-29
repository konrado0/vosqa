from datetime import datetime, timedelta
from django.utils.translation import ugettext as _
from forum.badges.base import AbstractBadge
from forum.models import Badge
from forum.actions import *
from forum.models import Vote, Flag

import settings

class QuestionViewBadge(AbstractBadge):
    abstract = True
    listen_to = (QuestionViewAction,)
    
    order = 2
    class_name = _(u"Questions")

    @property
    def description(self):
        return _('Asked a question with %s views') % str(self.nviews)

    def award_to(self, action):
        if action.node.extra_count == int(self.nviews):
            return action.node.author


class PopularQuestion(QuestionViewBadge):
    name = _('Popular Question')
    nviews = settings.POPULAR_QUESTION_VIEWS


class NotableQuestion(QuestionViewBadge):
    type = Badge.SILVER
    name = _('Famous Question')
    nviews = settings.NOTABLE_QUESTION_VIEWS

class FamousQuestion(QuestionViewBadge):
    type = Badge.GOLD
    name = _('Viral Question')
    nviews = settings.FAMOUS_QUESTION_VIEWS


class NodeScoreBadge(AbstractBadge):
    abstract = True
    listen_to = (VoteAction,)

    def award_to(self, action):
        if (action.node.node_type == self.node_type) and (action.node.score == int(self.expected_score)):
            return action.node.author


class QuestionScoreBadge(NodeScoreBadge):
    abstract = True
    node_type = "question"
    
    order = 1
    class_name = _(u"Questions")

    @property
    def description(self):
        return _('Question voted up %s times') % str(self.expected_score)

class NiceQuestion(QuestionScoreBadge):
    expected_score = settings.NICE_QUESTION_VOTES_UP
    name = _("Nice Question")

class GoodQuestion(QuestionScoreBadge):
    type = Badge.SILVER
    expected_score = settings.GOOD_QUESTION_VOTES_UP
    name = _("Good Question")

class GreatQuestion(QuestionScoreBadge):
    type = Badge.GOLD
    expected_score = settings.GREAT_QUESTION_VOTES_UP
    name = _("Great Question")


class AnswerScoreBadge(NodeScoreBadge):
    abstract = True
    node_type = "answer"
    
    order = 10
    class_name = _(u"Answers")

    @property
    def description(self):
        return _('Answer voted up %s times') % str(self.expected_score)

class NiceAnswer(AnswerScoreBadge):
    expected_score = settings.NICE_ANSWER_VOTES_UP
    name = _("Nice Answer")

class GoodAnswer(AnswerScoreBadge):
    type = Badge.SILVER
    expected_score = settings.GOOD_ANSWER_VOTES_UP
    name = _("Good Answer")

class GreatAnswer(AnswerScoreBadge):
    type = Badge.GOLD
    expected_score = settings.GREAT_ANSWER_VOTES_UP
    name = _("Perfect Answer")


class QuestionFavoritedBadge(AbstractBadge):
    abstract = True
    listen_to = (FavoriteAction,)
    
    order = 4
    class_name = _(u"Questions")

    @property
    def description(self):
        return _('Question favorited by %s users') % str(self.expected_count)

    def award_to(self, action):
        if (action.node.node_type == "question") and (action.node.favorite_count == int(self.expected_count)):
            return action.node.author

class FavoriteQuestion(QuestionFavoritedBadge):
    type = Badge.SILVER
    name = _("Favorite Question")
    expected_count = settings.FAVORITE_QUESTION_FAVS

class StellarQuestion(QuestionFavoritedBadge):
    type = Badge.GOLD
    name = _("Stellar Question")
    expected_count = settings.STELLAR_QUESTION_FAVS


# class Disciplined(AbstractBadge):
#     listen_to = (DeleteAction,)
#     name = _("Disciplined")
#     description = _('Deleted own post with score of %s or higher') % settings.DISCIPLINED_MIN_SCORE
# 
#     def award_to(self, action):
#         if (action.node.author == action.user) and (action.node.score >= int(settings.DISCIPLINED_MIN_SCORE)):
#             return action.user

# class PeerPressure(AbstractBadge):
#     listen_to = (DeleteAction,)
#     name = _("Peer Pressure")
#     description = _('Deleted own post with score of %s or lower') % settings.PEER_PRESSURE_MAX_SCORE
# 
#     def award_to(self, action):
#         if (action.node.author == action.user) and (action.node.score <= int(settings.PEER_PRESSURE_MAX_SCORE)):
#             return action.user

class ActivityBadge(AbstractBadge):
    order = 20
        
    abstract = True
    listen_to = (VoteUpAction, VoteDownAction)

    @property
    def description(self):
        return _('Voted %d times on answers/questions') % self.expected_count

    def award_to(self, action):
        if (action.user.vote_down_count + action.user.vote_up_count == self.expected_count):
            return action.user

class Enthusiast(ActivityBadge):
    award_once = True
    name = _("Enthusiast")
    expected_count = settings.ENTHUSIAST_VOTES_COUNT
    
class Fanatic(ActivityBadge):
    award_once = True
    type = Badge.SILVER
    name = _("Fanatic")
    expected_count = settings.FANATIC_VOTES_COUNT

class Maniac(ActivityBadge):
    award_once = True
    type = Badge.GOLD
    name = _("Maniac")
    expected_count = settings.MANIAC_VOTES_COUNT

class Critic(AbstractBadge):
    order = 22
        
    award_once = True
    listen_to = (VoteDownAction,)
    name = _("Critic")
    description = _('First down vote')

    def award_to(self, action):
        if (action.user.vote_down_count == 1):
            return action.user


class Supporter(AbstractBadge):
    order = 21
        
    award_once = True
    listen_to = (VoteUpAction,)
    name = _("Supporter")
    description = _('First up vote')

    def award_to(self, action):
        if (action.user.vote_up_count == 1):
            return action.user


class FirstActionBadge(AbstractBadge):
    award_once = True
    abstract = True

    def award_to(self, action):
        if (self.listen_to[0].objects.filter(user=action.user).count() == 1):
            return action.user

class CitizenPatrol(FirstActionBadge):
    listen_to = (FlagAction,)
    name = _("Citizen Patrol")
    description = _('First flagged post')

class Organizer(FirstActionBadge):
    listen_to = (RetagAction,)
    name = _("Organizer")
    description = _('First retag')

class Editor(FirstActionBadge):
    order = 40
    listen_to = (ReviseAction,)
    name = _("Editor")
    description = _('First edit')

class Scholar(FirstActionBadge):
    order = 5
    class_name = _(u"Questions")
    
    listen_to = (AcceptAnswerAction,)
    name = _("Scholar")
    description = _('First accepted answer on your own question')

# class Cleanup(FirstActionBadge):
#     listen_to = (RollbackAction,)
#     name = _("Cleanup")
#     description = _('First rollback')


class Autobiographer(AbstractBadge):
    award_once = True
    listen_to = (EditProfileAction,)
    name = _("Autobiographer")
    description = _('Completed all user profile fields')

    def award_to(self, action):
        user = action.user
        if user.email and user.real_name and user.website and user.location and \
                user.date_of_birth and user.about:
            return user


# class CivicDuty(AbstractBadge):
#     type = Badge.SILVER
#     award_once = True
#     listen_to = (VoteUpAction, VoteDownAction)
#     name = _("Civic Duty")
#     description = _('Voted %s times') % settings.CIVIC_DUTY_VOTES
# 
#     def award_to(self, action):
#         if (action.user.vote_up_count + action.user.vote_down_count) == int(settings.CIVIC_DUTY_VOTES):
#             return action.user

class CommentBadge(AbstractBadge):
    order = 30
    
    abstract = True
    award_once = True

class Pundit(CommentBadge):
    type = Badge.SILVER
    listen_to = (VoteUpCommentAction,)
    name = _("Pundit")
    description = _('Left %d comments voted up at least %d times') % (settings.PUNDIT_COMMENT_COUNT,settings.PUNDIT_VOTES_COUNT) 

    def award_to(self, action):
        if action.node.score == settings.PUNDIT_VOTES_COUNT and action.node.author.nodes.filter_state(deleted=False).filter(
                node_type="comment", score__gte=settings.PUNDIT_VOTES_COUNT).count() == settings.PUNDIT_COMMENT_COUNT:
            return action.node.author

class Commentator(CommentBadge):    
    listen_to = (CommentAction,)
    name = _("Commentator")
    description = _('Left %s comments') % settings.COMMENTATOR_COMMENT_COUNT

    def award_to(self, action):
        if action.user.nodes.filter_state(deleted=False).filter(node_type="comment").count() == int(
                settings.PUNDIT_COMMENT_COUNT):
            return action.user

class SelfLearner(AbstractBadge):
    order = 14
    class_name = _(u"Answers")
    
    listen_to = (VoteUpAction, )
    name = _("Self Learner")
    description = _('Answered your own question with at least %s up votes') % settings.SELF_LEARNER_UP_VOTES

    def award_to(self, action):
        if (action.node.node_type == "answer") and (action.node.author == action.node.parent.author) and (
        action.node.score == int(settings.SELF_LEARNER_UP_VOTES)):
            return action.node.author


class StrunkAndWhite(AbstractBadge):
    order = 40
    
    type = Badge.SILVER
    award_once = True
    listen_to = (ReviseAction,)
    name = _("Strunk & White")
    description = _('Edited %s entries') % settings.STRUNK_AND_WHITE_EDITS

    def award_to(self, action):
        if (ReviseAction.objects.filter(user=action.user).count() == int(settings.STRUNK_AND_WHITE_EDITS)):
            return action.user


class QuestionAsker(AbstractBadge):
    award_once = True
    abstract = True  
    listen_to = (VoteUpAction,)
    
    order = 0
    class_name = _(u"Questions")
    
    @property
    def description(self):
        return  _(u'Asked %d question%s with at least %d up vote%s') % (self.question_count, u"s" if self.question_count>1 else u"", 
                                                                        self.min_upvotes, u"s" if self.min_upvotes>1 else u"")

    def award_to(self, action):
        if (action.node.node_type == "question") and (action.node.author.nodes.filter_state(deleted=False).filter(
                node_type="question", score__gte=self.min_upvotes).count() == self.question_count):
            return action.node.author


class Student(QuestionAsker):
    name = _("Student")    
    question_count = settings.STUDENT_QUESTION_COUNT    
    min_upvotes = settings.STUDENT_MIN_UPVOTE
    
class Seeker(QuestionAsker):
    type = Badge.SILVER
    name = _("Seeker")    
    question_count = settings.SEEKER_QUESTION_COUNT    
    min_upvotes = settings.SEEKER_MIN_UPVOTE
    
class Hunter(QuestionAsker):
    type = Badge.GOLD
    name = _("Hunter")    
    question_count = settings.HUNTER_QUESTION_COUNT    
    min_upvotes = settings.HUNTER_MIN_UPVOTE


class Answerer(AbstractBadge):
    award_once = True
    abstract = True  
    listen_to = (VoteUpAction,)
    
    order = 9
    class_name = _(u"Answers")
    
    @property
    def description(self):
        return  _(u'Gave %d answers%s with at least %d up vote%s') % (self.answer_count, u"s" if self.answer_count>1 else u"", 
                                                                        self.min_upvotes, u"s" if self.min_upvotes>1 else u"")

    def award_to(self, action):
        if (action.node.node_type == "answer") and (action.node.author.nodes.filter_state(deleted=False).filter(
                node_type="answer", score__gte=self.min_upvotes).count() == self.answer_count):
            return action.node.author

class Teacher(Answerer):
    name = _("Helpmate")
    answer_count = settings.HELPMATE_ANSWER_COUNT    
    min_upvotes = settings.HELPMATE_MIN_UPVOTE
    
class Stylist(Answerer):
    type = Badge.SILVER
    name = _("Teacher")
    answer_count = settings.STYLIST_ANSWER_COUNT    
    min_upvotes = settings.STYLIST_MIN_UPVOTE
  
class Advisor(Answerer):
    type = Badge.GOLD
    name = _("Advisor")
    answer_count = settings.ADVISOR_ANSWER_COUNT    
    min_upvotes = settings.ADVISOR_MIN_UPVOTE

# class Enlightened(AbstractBadge):
#     type = Badge.SILVER
#     award_once = True
#     listen_to = (VoteUpAction, AcceptAnswerAction)
#     name = _("Enlightened")
#     description = _('First answer was accepted with at least %s up votes') % settings.ENLIGHTENED_UP_VOTES
# 
#     def award_to(self, action):
#         if (action.node.node_type == "answer") and (action.node.accepted) and (
#         action.node.score >= int(settings.ENLIGHTENED_UP_VOTES)):
#             return action.node.author


class Guru(AbstractBadge):
    order = 12
    class_name = _(u"Answers")
    
    type = Badge.SILVER
    listen_to = (VoteUpAction, AcceptAnswerAction)
    name = _("Guru")
    description = _('Accepted answer and voted up %s times') % settings.GURU_UP_VOTES

    def award_to(self, action):
        if (action.node.node_type == "answer") and (action.node.accepted) and (
        action.node.score >= int(settings.GURU_UP_VOTES)):
            return action.node.author


class Necromancer(AbstractBadge):
    order = 13
    class_name = _(u"Answers")
    
    type = Badge.SILVER
    listen_to = (VoteUpAction,)
    name = _("Necromancer")
    description = _('Answered a question more than %(dif_days)s days later with at least %(up_votes)s votes') % \
            {'dif_days': settings.NECROMANCER_DIF_DAYS, 'up_votes': settings.NECROMANCER_UP_VOTES}

    def award_to(self, action):
        if (action.node.node_type == "answer") and (
        action.node.added_at >= (action.node.question.added_at + timedelta(days=int(settings.NECROMANCER_DIF_DAYS)))
        ) and (int(action.node.score) == int(settings.NECROMANCER_UP_VOTES)):
            return action.node.author

# class Taxonomist(AbstractBadge):
#     type = Badge.SILVER
#     listen_to = tuple()
#     name = _("Taxonomist")
#     description = _('Created a tag used by %s questions') % settings.TAXONOMIST_USE_COUNT
# 
#     def award_to(self, action):
#         return None

# class ValidatedEmail(AbstractBadge):
#     type = Badge.BRONZE
#     listen_to = (EmailValidationAction,)
#     name = _("Validated Email")
#     description = _("User who has validated email associated to the account")
#     award_once = True
# 
#     def award_to(self, action):
#         return action.user

def get_badge_data(badge):
    b_class = globals()[badge.cls]
    badge.class_name = b_class.class_name
    badge.order = b_class.order    
    return badge

def badge_order(b1, b2):
    simple_order = cmp(b1.order, b2.order)
    if simple_order:
        return simple_order
    
    type_order = cmp(b1.type, b2.type)    
    return type_order if type_order else cmp(b1.name, b2.name)
