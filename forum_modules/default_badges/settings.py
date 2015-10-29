from forum.settings.base import Setting
from forum.settings.users import BADGES_SET
from django.utils.translation import ugettext_lazy as _

POPULAR_QUESTION_VIEWS = Setting('POPULAR_QUESTION_VIEWS', 1000, BADGES_SET, dict(
label = _("Popular Question views"),
help_text = _("""
Number of question views required to award a Popular Question badge to the question author
""")))

NOTABLE_QUESTION_VIEWS = Setting('NOTABLE_QUESTION_VIEWS', 2500, BADGES_SET, dict(
label = _("Notable Question views"),
help_text = _("""
Number of question views required to award a Notable Question badge to the question author
""")))

FAMOUS_QUESTION_VIEWS = Setting('FAMOUS_QUESTION_VIEWS', 10000, BADGES_SET, dict(
label = _("Famous Question views"),
help_text = _("""
Number of question views required to award a Famous Question badge to the question author
""")))

NICE_ANSWER_VOTES_UP = Setting('NICE_ANSWER_VOTES_UP', 10, BADGES_SET, dict(
label = _("Nice Answer up votes"),
help_text = _("""
Number of up votes required to award a Nice Answer badge to the answer author
""")))

NICE_QUESTION_VOTES_UP = Setting('NICE_QUESTION_VOTES_UP', 10, BADGES_SET, dict(
label = _("Nice Question up votes"),
help_text = _("""
Number of up votes required to award a Nice Question badge to the question author
""")))

GOOD_ANSWER_VOTES_UP = Setting('GOOD_ANSWER_VOTES_UP', 25, BADGES_SET, dict(
label = _("Good Answer up votes"),
help_text = _("""
Number of up votes required to award a Good Answer badge to the answer author
""")))

GOOD_QUESTION_VOTES_UP = Setting('GOOD_QUESTION_VOTES_UP', 25, BADGES_SET, dict(
label = _("Good Question up votes"),
help_text = _("""
Number of up votes required to award a Good Question badge to the question author
""")))

GREAT_ANSWER_VOTES_UP = Setting('GREAT_ANSWER_VOTES_UP', 100, BADGES_SET, dict(
label = _("Great Answer up votes"),
help_text = _("""
Number of up votes required to award a Great Answer badge to the answer author
""")))

GREAT_QUESTION_VOTES_UP = Setting('GREAT_QUESTION_VOTES_UP', 100, BADGES_SET, dict(
label = _("Great Question up votes"),
help_text = _("""
Number of up votes required to award a Great Question badge to the question author
""")))

FAVORITE_QUESTION_FAVS = Setting('FAVORITE_QUESTION_FAVS', 25, BADGES_SET, dict(
label = _("Favorite Question favorite count"),
help_text = _("""
How many times a question needs to be favorited by other users to award a Favorite Question badge to the question author
""")))

STELLAR_QUESTION_FAVS = Setting('STELLAR_QUESTION_FAVS', 100, BADGES_SET, dict(
label = _("Stellar Question favorite count"),
help_text = _("""
How many times a question needs to be favorited by other users to award a Stellar Question badge to the question author
""")))

ENTHUSIAST_VOTES_COUNT = Setting('ENTHUSIAST_VOTES_COUNT', 100, BADGES_SET, dict(
label = _("Enthusiast badge votes"),
help_text = _("""
How many times user needs to vote to get Enthusiast badge.
""")))

FANATIC_VOTES_COUNT = Setting('FANATIC_VOTES_COUNT', 500, BADGES_SET, dict(
label = _("Fanatic badge votes"),
help_text = _("""
How many times user needs to vote to get Fanatic badge.
""")))

MANIAC_VOTES_COUNT = Setting('MANIAC_VOTES_COUNT', 2500, BADGES_SET, dict(
label = _("Maniac badge votes"),
help_text = _("""
How many times user needs to vote to get Maniac badge.
""")))

# DISCIPLINED_MIN_SCORE = Setting('DISCIPLINED_MIN_SCORE', 3, BADGES_SET, dict(
# label = _("Disciplined minimum score"),
# help_text = _("""
# Minimum score a question needs to have to award the Disciplined badge to an author of a question who deletes it.
# """)))

# PEER_PRESSURE_MAX_SCORE = Setting('PEER_PRESSURE_MAX_SCORE', -3, BADGES_SET, dict(
# label = _("Peer Pressure maximum score"),
# help_text = _("""
# Maximum score a question needs to have to award the Peer Pressure badge to an author of a question who deletes it.
# """)))

# CIVIC_DUTY_VOTES = Setting('CIVIC_DUTY_VOTES', 300, BADGES_SET, dict(
# label = _("Civic Duty votes"),
# help_text = _("""
# Number of votes an user needs to cast to be awarded the Civic Duty badge.
# """)))

PUNDIT_COMMENT_COUNT = Setting('PUNDIT_COMMENT_COUNT', 10, BADGES_SET, dict(
label = _("Pundit number of comments"),
help_text = _("""
Number of comments an user needs to post to be awarded the Pundit badge.
""")))

PUNDIT_VOTES_COUNT = Setting('PUNDIT_VOTES_COUNT', 5, BADGES_SET, dict(
label = _("Pundit comment voteups"),
help_text = _("""
Number of votes comment has to receive to qualify to count in Pundit badge.
""")))

COMMENTATOR_COMMENT_COUNT = Setting('COMMENTATOR_COMMENT_COUNT', 10, BADGES_SET, dict(
label = _("Commentator number of comments"),
help_text = _("""
Number of comments an user needs to post to be awarded the Commentator badge.
""")))

SELF_LEARNER_UP_VOTES = Setting('SELF_LEARNER_UP_VOTES', 3, BADGES_SET, dict(
label = _("Self Learner up votes"),
help_text = _("""
Number of up votes an answer from the question author needs to have for the author to be awarded the Self Learner badge.
""")))

STRUNK_AND_WHITE_EDITS = Setting('STRUNK_AND_WHITE_EDITS', 100, BADGES_SET, dict(
label = _("Strunk and White updates"),
help_text = _("""
Number of question or answer updates an user needs to make to be awarded the Strunk & White badge.
""")))

# ENLIGHTENED_UP_VOTES = Setting('ENLIGHTENED_UP_VOTES', 10, BADGES_SET, dict(
# label = _("Enlightened up votes"),
# help_text = _("""
# Number of up votes an accepted answer needs to have for the author to be awarded the Enlightened badge.
# """)))

STUDENT_QUESTION_COUNT = Setting('STUDENT_QUESTION_COUNT', 1, BADGES_SET, dict(
label = _("Student question count"),
help_text = _("""
Number of questions asked by user and meeting votes criteria.
""")))

STUDENT_MIN_UPVOTE = Setting('STUDENT_MIN_UPVOTE', 1, BADGES_SET, dict(
label = _("Student min upvote"),
help_text = _("""
Number of upvotes needed for question to qualify for counting in Student badge.
""")))

SEEKER_QUESTION_COUNT = Setting('SEEKER_QUESTION_COUNT', 25, BADGES_SET, dict(
label = _("Seeker question count"),
help_text = _("""
Number of questions asked by user and meeting votes criteria.
""")))

SEEKER_MIN_UPVOTE = Setting('SEEKER_MIN_UPVOTE', 5, BADGES_SET, dict(
label = _("Seeker min upvote"),
help_text = _("""
Number of upvotes needed for question to qualify for counting in Seeker badge.
""")))

HUNTER_QUESTION_COUNT = Setting('HUNTER_QUESTION_COUNT', 100, BADGES_SET, dict(
label = _("Hunter question count"),
help_text = _("""
Number of questions asked by user and meeting votes criteria.
""")))

HUNTER_MIN_UPVOTE = Setting('HUNTER_MIN_UPVOTE', 5, BADGES_SET, dict(
label = _("Hunter min upvote"),
help_text = _("""
Number of upvotes needed for question to qualify for counting in Hunter badge.
""")))

HELPMATE_ANSWER_COUNT = Setting('HELPMATE_ANSWER_COUNT', 1, BADGES_SET, dict(
label = _("Helpmate answer count"),
help_text = _("""
Number of answers given by user and meeting votes criteria.
""")))

HELPMATE_MIN_UPVOTE = Setting('HELPMATE_MIN_UPVOTE', 1, BADGES_SET, dict(
label = _("Helpmate min upvote"),
help_text = _("""
Number of upvotes needed for answer to qualify for counting in Helpmate badge.
""")))

STYLIST_ANSWER_COUNT = Setting('STYLIST_ANSWER_COUNT', 20, BADGES_SET, dict(
label = _("Stylist answer count"),
help_text = _("""
Number of answers given by user and meeting votes criteria.
""")))

STYLIST_MIN_UPVOTE = Setting('STYLIST_MIN_UPVOTE', 3, BADGES_SET, dict(
label = _("Stylist min upvote"),
help_text = _("""
Number of upvotes needed for answer to qualify for counting in Stylist badge.
""")))

ADVISOR_ANSWER_COUNT = Setting('ADVISOR_ANSWER_COUNT', 50, BADGES_SET, dict(
label = _("Advisor answer count"),
help_text = _("""
Number of answers given by user and meeting votes criteria.
""")))

ADVISOR_MIN_UPVOTE = Setting('ADVISOR_MIN_UPVOTE', 5, BADGES_SET, dict(
label = _("Advisor min upvote"),
help_text = _("""
Number of upvotes needed for answer to qualify for counting in advisor badge.
""")))

GURU_UP_VOTES = Setting('GURU_UP_VOTES', 40, BADGES_SET, dict(
label = _("Guru up votes"),
help_text = _("""
Number of up votes an accepted answer needs to have for the author to be awarded the Guru badge.
""")))

NECROMANCER_UP_VOTES = Setting('NECROMANCER_UP_VOTES', 5, BADGES_SET, dict(
label = _("Necromancer up votes"),
help_text = _("""
Number of up votes an answer needs to have for the author to be awarded the Necromancer badge.
""")))

NECROMANCER_DIF_DAYS = Setting('NECROMANCER_DIF_DAYS', 60, BADGES_SET, dict(
label = _("Necromancer difference in days"),
help_text = _("""
Difference in days betwen the posted date of a question and an answer for the answer author to be awarded the Necromancer badge.
""")))

TAXONOMIST_USE_COUNT = Setting('TAXONOMIST_USE_COUNT', 100, BADGES_SET, dict(
label = _("Taxonomist usage count"),
help_text = _("""
How many usages a tag needs to have for the tag creator to be awarded the Taxonomist badge. 
""")))

