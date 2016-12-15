import requests, sys
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

class Genius(object):

    def __init__(self):
        self.search_url = "http://api.genius.com/search/"

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

    def get_lyrics(self, song, artist):
        # create header to pass to Genius API
        headers = {'Authorization': 'Bearer ' + self.client_access_token}
        # set search url
        search_url = self.search_url
        # set search parameters to variables
        song_title = song
        artist_name = artist
        # create dictionary for request type
        data = {'q': song_title}
        # search Genius api for the song
        response = requests.get(search_url, data=data, headers=headers)
        # check to make sure the request when through
        if not response.ok:
            # if reponse was an error, break and print error
            print response.text, '\n\n\n\n\n'
            print '--- ', response.status_code, ' ---'
            print '--- ', response.reason, ' ---'
            sys.exit()
        # else continue with the scripts
        # turn response to JSON
        json = response.json()
        # declare song info variable
        song_info = None
        # loop through all hits in response
        if json["response"]["hits"] is None:
            return 'No Hits', 'No Hits', 'No Hits'
        else:
            for hit in json["response"]["hits"]:
                # check if the 'hits' primary artist matches the artist we want
                if hit["result"]["primary_artist"]["name"] is None:
                    return 'No Artist', 'No Artist', 'No Artist'
                elif hit["result"]["primary_artist"]["name"] == artist_name:
                    # set song info variable
                    song_info = hit
                    # pull path to lyrics page from the hit
                    path = song_info['result']['path']
                    # create a path to the lyrics page
                    page_url = "http://genius.com" + path
                    #create a fake user agent
                    #ua = UserAgent()
                    #headers = {'User-Agent': ua.random}
                    # request the page
                    #page = requests.get(page_url, headers=headers)
                    page = requests.get(page_url)
                    # parse page's html
                    # pull lyrics from html
                    try:
                        html = BeautifulSoup(page.text, "html.parser")
                        lyrics = html.find("lyrics").text
                        html = html.text
                    except (AttributeError, TypeError) as e:
                        lyrics = 'Error'
                        html = 'Error'
                        song_info = 'Error'
                    # return the song_info's JSON, the page's HTML, and the song lyrics
                    return song_info, html, lyrics
                else:
                    return 'No Result', 'No Result', 'No Result'
