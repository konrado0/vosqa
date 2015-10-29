# -*- coding: utf-8 -*-
""" 
Implements pure server side signin flow:
https://developers.google.com/+/web/signin/redirect-uri-flow
https://developers.google.com/+/domains/authentication/scopes
https://developers.google.com/api-client-library/python/guide/aaa_oauth#OAuth2WebServerFlow
Django project for this:
https://github.com/rochapps/django-google-oauth/blob/master/google_oauth/
https://github.com/jordanjambazov/osqa-gplus
"""
import string
import random
import logging
from json import load as load_json
from urllib import urlopen,  urlencode

from oauth2client.client import OAuth2WebServerFlow
from oauth2client.client import FlowExchangeError

from django.utils.encoding import smart_unicode
from django.conf import settings as django_settings
import settings
from forum.authentication.base import AuthenticationConsumer
from forum.authentication.base import ConsumerTemplateContext
from forum.authentication.base import InvalidAuthentication

scopes = "  ".join(("https://www.googleapis.com/auth/plus.login",
          "https://www.googleapis.com/auth/plus.profile.emails.read"))

class GoogleAuthConsumer(AuthenticationConsumer):
    
    @staticmethod
    def _get_flow():
        return OAuth2WebServerFlow(client_id=settings.GOOGLE_CONSUMER_KEY, 
                                     client_secret=settings.GOOGLE_CONSUMER_SECRET,
                                     redirect_uri='{0}/account/google/done/'.format(django_settings.APP_AUTH_URL),
                                     scope = scopes )

    @staticmethod
    def _generate_random_state():
        """
        Generates a random string with length of 32 symbols, used by the
        Google+ API to prevent request forgery.
        """
        symbols = string.ascii_lowercase + string.digits
        state = ''.join(random.choice(symbols) for _ in range(32))
        return state

    def prepare_authentication_request(self, request, redirect_to):
        """
        Prepares the Google+ authentication URL and adds needed parameters
        to it, like scopes, the generated state, client ID, etc.
        """
        state = self._generate_random_state()
        request.session['gplus_state'] = state
        flow = self._get_flow()
        flow.params['state'] = state
        return flow.step1_get_authorize_url()

    def process_authentication_request(self, request):
        """
        Triggered after the Google+ authentication happened. Important
        information from it is extracted, access token and association
        keys are obtained, so that local authentication system could
        process.
        """
        request_state = request.GET['state']
        session_state = request.session['gplus_state']
        del request.session['gplus_state']
        if request_state != session_state:
            logging.error("Google auth state did not match during request authentication")
            raise InvalidAuthentication("Request State Did Not Match")
        code = request.GET['code']
        try:
            # Upgrade the authorization code into a credentials object
            flow = self._get_flow()
            credentials = flow.step2_exchange(code)
        except FlowExchangeError:
            logging.exception("Exception during Google+ auth flow exchange")
            raise InvalidAuthentication("Could not exchange flows")
        assoc_key = credentials.id_token['sub']
        request.session["access_token"] = credentials.access_token
        request.session["assoc_key"] = assoc_key
        return assoc_key

    def get_user_data(self, access_token):
        """
        Returns user data, like username, email and real name. That data
        is forwarded to the sign-up form.
        """
        profile = load_json(urlopen("https://www.googleapis.com/plus/v1/people/me?" + urlencode(dict(access_token=access_token))))

        name = smart_unicode(profile.get(u'displayName', u""));
        if len(name) == 0:
            logging.warning(u"Unable to get name from Google+, profile returned: %s" % unicode(profile))
        # If the name is longer than 30 characters - leave it blank
        if len(name) > 30:
            name = ''

        # Check whether the length if the email is greater than 75, if it is -- just replace the email
        # with a blank string variable, otherwise we're going to have trouble with the Django model.
        email = u''
        emails = profile.get(u'emails', [])
        if emails:
            tmp_email = None
            for e in emails:
                if e[u'type'] == u'account':
                    email = smart_unicode(e[u'value'])
                    break
                else:
                    tmp_email = smart_unicode(e[u'value'])
            if not email:
                email = tmp_email
        if len(email) == 0:
            logging.warning(u"Unable to get email from Google+, profile returned: %s" % unicode(profile))
        if len(email) > 75:
            email = u''

        # Return the user data.
        return {
            'id' : profile.get(u'id', u''),
            'username': name,
            'email': email,
        }

class GoogleAuthContext(ConsumerTemplateContext):
    mode = 'BIGICON'
    type = 'DIRECT'
    weight = 150
    human_name = 'Google'
    icon = '/media/images/openid/google.gif'
#     code_template = 'modules/gplusauth/button.html'
#     extra_css = []
