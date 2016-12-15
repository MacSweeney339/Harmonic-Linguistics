from spotipy import Spotify
import spotipy.util as util
import base64
from Spotify_Credentials import Spotify_Credentials

spot_creds = Spotify_Credentials()
token = util.prompt_for_user_token(spot_creds.user_id, None, spot_creds.client_id, spot_creds.client_secret, spot_creds.redirect_uri)
spotify = Spotify(auth=code)
