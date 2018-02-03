#!/usr/bin/python

from requests_oauthlib import OAuth2Session

# Application configutation
client_id     = 'CBJCHBCAABAAgAfIaHGyanFH3GBNZMVk94AGRkagLoh-'
client_secret = 'PbV0cUkRruvJqRi7-yFnCra12BXm7XjX'
redirect_uri  = 'https://example.com'
scope         = ['user_login:self',
                 'agreement_send:account']
token_url     = 'https://secure.na2.echosign.com/oauth/token'

# User authorization through redirection
oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope, state=None)
auth_url, state = oauth.authorization_url('https://secure.na2.echosign.com/public/oauth?redirect_uri=https://example.com')

# Print authorization url  and ask for user access url
print("\nPlease visit:\n{}\nand authorize access.".format(auth_url))
auth_responses = input("\nEnter full callback URL:\n")

# Fetch access token
token = oauth.fetch_token(token_url=token_url, authorization_response=auth_responses, client_secret=client_secret)

print(token)


