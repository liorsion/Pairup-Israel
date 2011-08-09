
# LinkedIn configuration
LINKEDIN_SERVER = 'api.linkedin.com'
LINKEDIN_AUTHORIZATION_URL = 'https://%s/oauth/authorize' % LINKEDIN_SERVER
LINKEDIN_ACCESS_TOKEN_URL = 'https://%s/oauth/access_token' % LINKEDIN_SERVER
LINKEDIN_CHECK_AUTH = 'https://%s/me' % LINKEDIN_SERVER
EXPIRES_NAME = getattr(settings, 'SOCIAL_AUTH_EXPIRATION', 'expires')

class LinkedInAPI(object):
    
    def __init__(self, consumer_key, consumer_secret):
        self.consumer_key = ck
        self.consumer_secret = cs
        
    def get_user_profile(self, access_token, selectors=None, **kwargs):
        assert type(selectors) == "list", '"Keyword argument "selectors" must be of type "list"'
        user_token, url = self.prepare_request(access_token, self.api_profile_url, kwargs)
        client = oauth.Client(self.consumer, user_token)
        
        if not selectors:
            resp, content = client.request(self.api_profile_url, 'GET')
        else:
            url = self.prepare_field_selectors(selectors, url)
            resp, content = client.request(url, 'GET')
        
        content = self.clean_dates(content)
        return LinkedInXMLParser(content).results
    
    def prepare_request(self, access_token, url, kws=[]):
        user_token = oauth.Token(access_token['oauth_token'],
                        access_token['oauth_token_secret'])
        prep_url = url
        if kws and 'id' in kws.keys():
            prep_url = self.append_id_args(kws['id'], prep_url)
            del kws['id']
        for k in kws:
            if kws[k]:
                if '?' not in prep_url:
                    prep_url = self.append_initial_arg(k, kws[k], prep_url)
                else:
                    prep_url = self.append_sequential_arg(k, kws[k], prep_url)
        prep_url = re.sub('&&', '&', prep_url)
        print prep_url
        return user_token, prep_url