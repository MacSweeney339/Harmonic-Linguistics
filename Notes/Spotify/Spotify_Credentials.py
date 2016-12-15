class Spotify_Credentials(object):

    def __init__(self):
        self.base_url = "https://api.spotify.com"

        # read in api key file
        key_array = []
        with open('SpotifyKey') as f:
            for line in f:
                key_array.append(line.replace('\n',''))
        # turn list into dict
        key_dict = {}
        for item in key_array:
            key, value = item.split(',')
            setattr(self, key, value)
