from consumer import OAuthAbstractAuthConsumer
from forum.authentication.base import ConsumerTemplateContext

import settings

class TwitterAuthConsumer(OAuthAbstractAuthConsumer):
    def __init__(self):
        OAuthAbstractAuthConsumer.__init__(self,
                str(settings.TWITTER_CONSUMER_KEY),
                str(settings.TWITTER_CONSUMER_SECRET),
                "twitter.com",
                "https://api.twitter.com/oauth/request_token",
                "https://api.twitter.com/oauth/access_token",
                "https://api.twitter.com/oauth/authenticate",
        )

    def get_user_data(self, key):
        json = self.fetch_data(key, "https://twitter.com/account/verify_credentials.json")
        
        if 'screen_name' in json:
            creds = json.loads(json)

            return {
                'username': creds['screen_name']
            }
        
        
        return {}

class TwitterAuthContext(ConsumerTemplateContext):
    mode = 'BIGICON'
    type = 'DIRECT'
    weight = 200
    human_name = 'Twitter'
    icon = '/media/images/openid/twitter.png'