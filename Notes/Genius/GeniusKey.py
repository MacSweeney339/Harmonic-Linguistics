from sanction.client import Client
import time
import requests

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
