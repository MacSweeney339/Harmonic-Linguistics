
from sanction.client import Client

class Genius(object):

    def __init__(self):

    def get_genius_key(self):
        # read in api key file
        key_array = []
        with open('GeniusKey') as f:
            for line in f:
                key_array.append(line.replace('\n',''))
        # turn list into dict
        key_dict = {}
        for item in key_array:
            key, value = item.split(',')
            setattr(self, key, value)

    def authenticate_genius(self):
    # THESE LINES GIVE EXAMPLE CODE FOR AUTHENTICATING USERS WHO LOG IN TO THE APP

        from sanction.client import Client
        # instantiating a client to get the auth URI
        c = Client(auth_endpoint="https://api.genius.com/oauth/authorize",
            client_id=config["google.client_id"],
            redirect_uri="http://localhost:8080/login/google")

    # instantiating a client to process OAuth2 response
        c = Client(token_endpoint="https://accounts.google.com/o/oauth2/token",
            resource_endpoint="https://www.googleapis.com/oauth2/v1",
            redirect_uri="http://localhost:8080/login/google",
            client_id=config["google.client_id"],
            client_secret=config["google.client_secret"])

GET /some-endpoint HTTP/1.1
User-Agent: CompuServe Classic/1.22
Accept: application/json
Host: api.genius.com
Authorization: Bearer ACCESS_TOKEN
