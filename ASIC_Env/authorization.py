from requests_oauthlib import OAuth2Session

# Application configutation
client_id     = 'CBJCHBCAABAAgAfIaHGyanFH3GBNZMVk94AGRkagLoh-'
client_secret = 'PbV0cUkRruvJqRi7-yFnCra12BXm7XjX'
redirect_uri  = 'https://example.com'
scope         = ['user_login:self', 'agreement_send:account']
token_url     = 'https://secure.na2.echosign.com/oauth/token'
auth_url      = ""
oauth         = ""


def authorization():

    global auth_url
    global oauth

    # User authorization through redirection
    oauth = OAuth2Session(client_id, redirect_uri=redirect_uri,
                          scope=scope, state=None)
    auth_url, state = oauth.authorization_url('https://secure.na2.echosign.com/public/oauth?redirect_uri=https://example.com')

    auth_url = auth_url

    return auth_url

def get_token(auth_responses):

    # Fetch access token
    token = oauth.fetch_token(token_url=token_url, authorization_response=auth_responses,
                              client_secret=client_secret)

    return token