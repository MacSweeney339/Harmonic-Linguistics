# Import packages to interface with MongoDB and Spotify API
from __future__ import division
import spotipy, sys, base64, time
from pymongo import MongoClient
from spotipy import Spotify, util, oauth2
from Spotify_Credentials import Spotify_Credentials

# print fun starting message
print "Ready...\n"
time.sleep(2)
print "Fight!"

# capture start time
start_time = time.time()

# Get Spotify Credentials from file
spot_creds = Spotify_Credentials()

# connect to MongoDB collections
prod_client = MongoClient()
prod_mack = prod_client['mack']
prod_musician = prod_mack['musician']
prod_album = prod_mack['album']
prod_song = prod_mack['song']

def get_musician_scope():
    #return [prod_musician.find_one()]
    return prod_musician.find({'spotify_data': {'$exists': False}}).batch_size(1500)

# pull all musicians without spotify data from Mnongo

Musician_Scope = get_musician_scope()

for musician in Musician_Scope:

    # capture start time
    musician_start_time = time.time()

    # Oauth@ Authenticate with Spotify
    authorization = spotipy.oauth2.SpotifyClientCredentials(spot_creds.client_id, spot_creds.client_secret)

    # Get access token
    access_token = authorization.get_access_token()

    # Create a spotify client Object
    spotify = Spotify(auth=access_token)

    # Search for artist using spotify client
    musician_results = spotify.search(q='artist:' + musician['musician_name'], type='artist')

    # Capture top result & time to get it
    if musician_results['artists']['items'] == []:

        prod_musician.update_one({'_id': musician['_id']}, {'$set': {'spotify_data': 'No Results'}})

    else:
        top_result = musician_results['artists']['items'][0]
        # update musician collection with spotify data
        prod_musician.update_one({'_id': musician['_id']}, {'$set': {'spotify_data': top_result}})

        # take artist id from top result and get artist albums
        albums = spotify.artist_albums(top_result['id'])

        # add albums and tracks to mongodb collections
        for album in albums['items']:

            # insert into album collection
            prod_album.insert_one({'musician_id': musician['_id'], 'spotify_artist_id': top_result['id'], \
                                   'spotify_album_data': album})

            # wait then take id from album and get album tracks
            tracks = spotify.album_tracks(album['id'])

            for track in tracks['items']:
                # use an exception to handle when a song doesn't have audio features
                try:
                    # capture audio features
                    audio_features = spotify.audio_features([track['id']])
                except ValueError:
                    # set audio features to no results
                    audio_features = 'No Results'

                # insert track and audio features into song collection
                prod_song.insert_one({'musician_id': musician['_id'], 'spotify_artist_id': top_result['id'], \
                                     'spotify_album_id': album['id'], 'spotify_track_data': track, \
                                     'audio_features': audio_features})

    # update status of collection musician for spotify data
    # capture & print out how long artist took to complete
    capture_time = round(time.time() - musician_start_time,2)
    process_time = round(time.time() - start_time, 2)
    musicians_updated = prod_musician.count({'spotify_data': {'$exists': True}})
    musicians_left = prod_musician.count({'spotify_data': {'$exists': False}})
    print "\n"
    print "--- {} musicians added & {} left to go ---".format(musicians_updated, musicians_left)
    print "--- last musician took {} seconds ---".format(capture_time)
    print "\n"

print "--- Data collection complete. ---"
print "\n"
