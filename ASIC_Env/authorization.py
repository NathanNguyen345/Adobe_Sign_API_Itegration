"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    This is our authorization process. It stores all the application keys as global variables. There's two
    functions that associate itself with this file. Authorization for permission to access the adobe application
    on the user's behalf and token retrieval.
    Written By: Nathan Nguyen
    Date: 2/2/2018
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
from requests_oauthlib import OAuth2Session

# Global variables for application configuration
client_id     = ""
client_secret = ""
redirect_uri  = 'https://example.com'
scope         = ['user_login:self', 'agreement_send:account']
token_url     = 'https://secure.na2.echosign.com/oauth/token'
auth_url      = ""
oauth         = ""


def authorization():
    """
    This function will authorize the client with the adobe server. A call back token is needed to
    confirm that the user has permission to access the server on behalf of the sender.
    :return: auth_url: authorization link to give client access and permission to the server
    """

    global auth_url
    global oauth

    # User authorization through redirection
    oauth = OAuth2Session(client_id, redirect_uri=redirect_uri,
                          scope=scope, state=None)
    auth_url, state = oauth.authorization_url('https://secure.na2.echosign.com/public/oauth?redirect_uri=https://example.com')

    auth_url = auth_url

    return auth_url

def get_token(auth_responses):
    """
    This function will return the the access token to the client to be saved and use for api calls
    :param auth_responses:
    :return: token: Access token to be used for api calls
    """

    # Fetch access token
    token = oauth.fetch_token(token_url=token_url, authorization_response=auth_responses,
                              client_secret=client_secret)

    return token
