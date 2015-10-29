# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import forum.models.utils
import datetime
import forum.models.resized_image_field
import forum.utils.time
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.CharField(max_length=39)),
                ('action_type', models.CharField(max_length=32)),
                ('action_date', models.DateTimeField(default=datetime.datetime.now)),
                ('extra', forum.models.utils.PickledObjectField(null=True, editable=False)),
                ('canceled', models.BooleanField(default=False)),
                ('canceled_at', models.DateTimeField(null=True)),
                ('canceled_ip', models.CharField(max_length=39)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ActionRepute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(default=datetime.datetime.now)),
                ('value', models.IntegerField(default=0)),
                ('by_canceled', models.BooleanField(default=False)),
                ('action', models.ForeignKey(related_name=b'reputes', to='forum.Action')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AuthKeyUserAssociation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(unique=True, max_length=255)),
                ('provider', models.CharField(max_length=64)),
                ('added_at', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Award',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('awarded_at', models.DateTimeField(default=datetime.datetime.now)),
                ('action', models.OneToOneField(related_name=b'award', to='forum.Action')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Badge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.SmallIntegerField()),
                ('cls', models.CharField(max_length=50, null=True)),
                ('awarded_count', models.PositiveIntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Flag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('reason', models.CharField(max_length=300)),
                ('flagged_at', models.DateTimeField(default=datetime.datetime.now)),
                ('action', models.OneToOneField(related_name=b'flag', to='forum.Action')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='KeyValue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(unique=True, max_length=255)),
                ('value', forum.models.utils.PickledObjectField(null=True, editable=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MarkedTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('reason', models.CharField(max_length=16, choices=[(b'good', 'interesting'), (b'bad', 'ignored')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=300)),
                ('tagnames', models.CharField(max_length=125)),
                ('body', models.TextField()),
                ('image', forum.models.resized_image_field.ResizableImageField(upload_to=forum.models.resized_image_field.GetName(b'upfiles/'))),
                ('node_type', models.CharField(default=b'node', max_length=16)),
                ('added_at', models.DateTimeField(default=datetime.datetime.now)),
                ('score', models.IntegerField(default=0)),
                ('state_string', models.TextField(default=b'')),
                ('last_activity_at', models.DateTimeField(null=True, blank=True)),
                ('extra', forum.models.utils.PickledObjectField(null=True, editable=False)),
                ('extra_count', models.IntegerField(default=0)),
                ('marked', models.BooleanField(default=False)),
                ('abs_parent', models.ForeignKey(related_name=b'all_children', to='forum.Node', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NodeRevision',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=300)),
                ('tagnames', models.CharField(max_length=125)),
                ('body', models.TextField()),
                ('image', forum.models.resized_image_field.ResizableImageField(upload_to=forum.models.resized_image_field.GetName(b'upfiles/'))),
                ('summary', models.CharField(max_length=300)),
                ('revision', models.PositiveIntegerField()),
                ('revised_at', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NodeState',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state_type', models.CharField(max_length=16)),
                ('action', models.OneToOneField(related_name=b'node_state', to='forum.Action')),
                ('node', models.ForeignKey(related_name=b'states', to='forum.Node')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OpenIdAssociation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('server_url', models.TextField(max_length=2047)),
                ('handle', models.CharField(max_length=255)),
                ('secret', models.TextField(max_length=255)),
                ('issued', models.IntegerField()),
                ('lifetime', models.IntegerField()),
                ('assoc_type', models.TextField(max_length=64)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OpenIdNonce',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('server_url', models.URLField()),
                ('timestamp', models.IntegerField()),
                ('salt', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QuestionSubscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('auto_subscription', models.BooleanField(default=True)),
                ('last_view', models.DateTimeField(default=datetime.datetime(2014, 9, 12, 11, 44, 5, 596876))),
                ('question', models.ForeignKey(to='forum.Node')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SubscriptionSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('enable_notifications', models.BooleanField(default=True)),
                ('member_joins', models.CharField(default=b'n', max_length=1)),
                ('new_question', models.CharField(default=b'n', max_length=1)),
                ('new_question_watched_tags', models.CharField(default=b'i', max_length=1)),
                ('subscribed_questions', models.CharField(default=b'i', max_length=1)),
                ('all_questions', models.BooleanField(default=False)),
                ('all_questions_watched_tags', models.BooleanField(default=False)),
                ('questions_viewed', models.BooleanField(default=False)),
                ('notify_answers', models.BooleanField(default=True)),
                ('notify_reply_to_comments', models.BooleanField(default=True)),
                ('notify_comments_own_post', models.BooleanField(default=True)),
                ('notify_comments', models.BooleanField(default=False)),
                ('notify_accepted', models.BooleanField(default=False)),
                ('send_digest', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now, null=True, blank=True)),
                ('used_count', models.PositiveIntegerField(default=0)),
            ],
            options={
                'ordering': ('-used_count', 'name'),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('is_approved', models.BooleanField(default=False)),
                ('email_isvalid', models.BooleanField(default=False)),
                ('reputation', models.IntegerField(default=0)),
                ('gold', models.PositiveIntegerField(default=0)),
                ('silver', models.PositiveIntegerField(default=0)),
                ('bronze', models.PositiveIntegerField(default=0)),
                ('last_seen', models.DateTimeField(default=datetime.datetime.now)),
                ('real_name', models.CharField(max_length=100, blank=True)),
                ('website', models.URLField(blank=True)),
                ('location', models.CharField(max_length=100, blank=True)),
                ('date_of_birth', models.DateField(null=True, blank=True)),
                ('about', models.TextField(blank=True)),
                ('avatar', forum.models.resized_image_field.ResizableImageField(null=True, upload_to=forum.models.resized_image_field.GetName(b'avatar/'), blank=True)),
                ('subscriptions', models.ManyToManyField(related_name=b'subscribers', through='forum.QuestionSubscription', to='forum.Node')),
            ],
            options={
            },
            bases=('auth.user', models.Model),
        ),
        migrations.CreateModel(
            name='UserProperty',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=16)),
                ('value', forum.models.utils.PickledObjectField(null=True, editable=False)),
                ('user', models.ForeignKey(related_name=b'properties', to='forum.User')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ValidationHash',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hash_code', models.CharField(unique=True, max_length=255)),
                ('seed', models.CharField(max_length=12)),
                ('expiration', models.DateTimeField(default=forum.utils.time.one_day_from_now)),
                ('type', models.CharField(max_length=12)),
                ('user', models.ForeignKey(to='forum.User')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.SmallIntegerField()),
                ('voted_at', models.DateTimeField(default=datetime.datetime.now)),
                ('action', models.OneToOneField(related_name=b'vote', to='forum.Action')),
                ('node', models.ForeignKey(related_name=b'votes', to='forum.Node')),
                ('user', models.ForeignKey(related_name=b'votes', to='forum.User')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together=set([('user', 'node')]),
        ),
        migrations.AlterUniqueTogether(
            name='validationhash',
            unique_together=set([('user', 'type')]),
        ),
        migrations.AlterUniqueTogether(
            name='userproperty',
            unique_together=set([('user', 'key')]),
        ),
        migrations.AddField(
            model_name='tag',
            name='created_by',
            field=models.ForeignKey(related_name=b'created_tags', to='forum.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tag',
            name='marked_by',
            field=models.ManyToManyField(related_name=b'marked_tags', through='forum.MarkedTag', to='forum.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='subscriptionsettings',
            name='user',
            field=models.OneToOneField(related_name=b'subscription_settings', editable=False, to='forum.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='questionsubscription',
            name='user',
            field=models.ForeignKey(to='forum.User'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='nodestate',
            unique_together=set([('node', 'state_type')]),
        ),
        migrations.AddField(
            model_name='noderevision',
            name='author',
            field=models.ForeignKey(related_name=b'noderevisions', to='forum.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='noderevision',
            name='node',
            field=models.ForeignKey(related_name=b'revisions', to='forum.Node'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='noderevision',
            unique_together=set([('node', 'revision')]),
        ),
        migrations.AddField(
            model_name='node',
            name='active_revision',
            field=models.OneToOneField(related_name=b'active', null=True, to='forum.NodeRevision'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='node',
            name='author',
            field=models.ForeignKey(related_name=b'nodes', to='forum.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='node',
            name='extra_ref',
            field=models.ForeignKey(to='forum.Node', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='node',
            name='last_activity_by',
            field=models.ForeignKey(to='forum.User', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='node',
            name='last_edited',
            field=models.ForeignKey(related_name=b'edited_node', null=True, to='forum.Action', unique=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='node',
            name='parent',
            field=models.ForeignKey(related_name=b'children', to='forum.Node', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='node',
            name='tags',
            field=models.ManyToManyField(related_name=b'nodes', to='forum.Tag'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='markedtag',
            name='tag',
            field=models.ForeignKey(related_name=b'user_selections', to='forum.Tag'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='markedtag',
            name='user',
            field=models.ForeignKey(related_name=b'tag_selections', to='forum.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='flag',
            name='node',
            field=models.ForeignKey(related_name=b'flags', to='forum.Node'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='flag',
            name='user',
            field=models.ForeignKey(related_name=b'flags', to='forum.User'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='flag',
            unique_together=set([('user', 'node')]),
        ),
        migrations.AddField(
            model_name='badge',
            name='awarded_to',
            field=models.ManyToManyField(related_name=b'badges', through='forum.Award', to='forum.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='award',
            name='badge',
            field=models.ForeignKey(related_name=b'awards', to='forum.Badge'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='award',
            name='node',
            field=models.ForeignKey(to='forum.Node', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='award',
            name='trigger',
            field=models.ForeignKey(related_name=b'awards', to='forum.Action', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='award',
            name='user',
            field=models.ForeignKey(to='forum.User'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='award',
            unique_together=set([('user', 'badge', 'node')]),
        ),
        migrations.AddField(
            model_name='authkeyuserassociation',
            name='user',
            field=models.ForeignKey(related_name=b'auth_keys', to='forum.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='actionrepute',
            name='user',
            field=models.ForeignKey(related_name=b'reputes', to='forum.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='action',
            name='canceled_by',
            field=models.ForeignKey(related_name=b'canceled_actions', to='forum.User', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='action',
            name='node',
            field=models.ForeignKey(related_name=b'actions', to='forum.Node', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='action',
            name='real_user',
            field=models.ForeignKey(related_name=b'proxied_actions', to='forum.User', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='action',
            name='user',
            field=models.ForeignKey(related_name=b'actions', to='forum.User'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='ActionProxy',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('forum.action',),
        ),
        migrations.CreateModel(
            name='AcceptAnswerAction',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('forum.actionproxy',),
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
            ],
            options={
                'abstract': False,
                'proxy': True,
            },
            bases=('forum.node',),
        ),
        migrations.CreateModel(
            name='AnswerRevision',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('forum.noderevision',),
        ),
        migrations.CreateModel(
            name='AnswerToCommentAction',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('forum.actionproxy',),
        ),
        migrations.CreateModel(
            name='AwardAction',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('forum.actionproxy',),
        ),
        migrations.CreateModel(
            name='AwardPointsAction',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('forum.actionproxy',),
        ),
        migrations.CreateModel(
            name='BonusRepAction',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('forum.actionproxy',),
        ),
        migrations.CreateModel(
            name='CloseAction',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('forum.actionproxy',),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
            ],
            options={
                'ordering': ('-added_at',),
                'abstract': False,
                'proxy': True,
            },
            bases=('forum.node',),
        ),
        migrations.CreateModel(
            name='CommentAction',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('forum.actionproxy',),
        ),
        migrations.CreateModel(
            name='CommentToAnswerAction',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('forum.actionproxy',),
        ),
        migrations.CreateModel(
            name='DeleteAction',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('forum.actionproxy',),
        ),
        migrations.CreateModel(
            name='EditPageAction',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('forum.actionproxy',),
        ),
        migrations.CreateModel(
            name='EditProfileAction',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('forum.actionproxy',),
        ),
        migrations.CreateModel(
            name='EmailValidationAction',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('forum.actionproxy',),
        ),
        migrations.CreateModel(
            name='FavoriteAction',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('forum.actionproxy',),
        ),
        migrations.CreateModel(
            name='FlagAction',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('forum.actionproxy',),
        ),
        migrations.CreateModel(
            name='NewPageAction',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('forum.actionproxy',),
        ),
        migrations.CreateModel(
            name='NodeEditAction',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('forum.actionproxy',),
        ),
        migrations.CreateModel(
            name='CommentToQuestionAction',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('forum.nodeeditaction',),
        ),
        migrations.CreateModel(
            name='AskAction',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('forum.nodeeditaction',),
        ),
        migrations.CreateModel(
            name='AnswerToQuestionAction',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('forum.nodeeditaction',),
        ),
        migrations.CreateModel(
            name='AnswerAction',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('forum.nodeeditaction',),
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
            ],
            options={
                'abstract': False,
                'proxy': True,
            },
            bases=('forum.node',),
        ),
        migrations.CreateModel(
            name='PublishAction',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('forum.actionproxy',),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
            ],
            options={
                'abstract': False,
                'proxy': True,
            },
            bases=('forum.node',),
        ),
        migrations.CreateModel(
            name='QuestionRevision',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('forum.noderevision',),
        ),
        migrations.CreateModel(
            name='ReportAction',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('forum.actionproxy',),
        ),
        migrations.CreateModel(
            name='RetagAction',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('forum.actionproxy',),
        ),
        migrations.CreateModel(
            name='ReviseAction',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('forum.nodeeditaction',),
        ),
        migrations.CreateModel(
            name='RollbackAction',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('forum.actionproxy',),
        ),
        migrations.CreateModel(
            name='SuspendAction',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('forum.actionproxy',),
        ),
        migrations.CreateModel(
            name='UnknownAction',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('forum.actionproxy',),
        ),
        migrations.CreateModel(
            name='UserJoinsAction',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('forum.actionproxy',),
        ),
        migrations.CreateModel(
            name='UserLoginAction',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('forum.actionproxy',),
        ),
        migrations.CreateModel(
            name='VoteAction',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('forum.actionproxy',),
        ),
        migrations.CreateModel(
            name='VoteDownAction',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('forum.voteaction',),
        ),
        migrations.CreateModel(
            name='VoteUpAction',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('forum.voteaction',),
        ),
        migrations.CreateModel(
            name='VoteUpCommentAction',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('forum.voteupaction',),
        ),
        migrations.CreateModel(
            name='WikifyAction',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('forum.actionproxy',),
        ),
    ]
