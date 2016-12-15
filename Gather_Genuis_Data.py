# Import packages to interface with MongoDB and Spotify API
from __future__ import division
import random, sys, base64, time, requests, socket, socks
from pymongo import MongoClient
from GeniusKey import Genius

import requests, sys
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

def go_spy_mode():
    socks.setdefaultproxy(proxy_type=socks.PROXY_TYPE_SOCKS5, addr="127.0.0.1", port=9050)
    socket.socket = socks.socksocket

def get_song_scope():
    # get songs without lyrics
    song_list = [song for song in prod_song.find({'genius_data': {'$exists': False}})]
    return song_list

def update_song_lyrics(song_id, hit, html, lyrics, process_time):
    prod_song.update_one({'_id': song_id}, {'$set' : {'genius_data': hit, 'html': html, 'lyrics': lyrics, 'process_time': process_time}})

def get_musician_name(musician_id):
    return prod_musician.find_one({'_id': musician_id})['musician_name']

def gather_lyrics(song):
    # create variables needed to use functions
    start_time = time.time()
    song_id = song['_id']
    song_title = song['spotify_track_data']['name']
    musician_name = get_musician_name(song['musician_id'])
    genius = Genius()

    # get song data
    hit, html, lyrics = genius.get_lyrics(song_title, musician_name)
    process_time = round(time.time() - start_time, 2)

    #update song
    update_song_lyrics(song_id, hit, html, lyrics, process_time)

    # update user with script status
    all_songs = prod_song.find({'genius_data': {'$exists': True}}).count()
    songs_with_lyrics = prod_song.find({'genius_data': {'$exists': True}, 'lyrics': {'$nin': ['No Result','AttributeError', 'TypeError']}}).count()
    print '--- updated song "', song_title, '" by "', musician_name, '" - with lyrics. Update took ', process_time, ' seconds ---'
    print '\n'
    print '--- {} song lyrics successfully added out of {} songs ---'.format(songs_with_lyrics, all_songs)


# print fun starting message
print "Ready...\n"
time.sleep(2)
print "Fight!"

# connect to MongoDB
prod_client = MongoClient()
prod_mack = prod_client['mack']
prod_musician = prod_mack['musician']
prod_song = prod_mack['song']

# anonymize requests
#go_spy_mode()

# get list of songs to update
start_time = time.time()
song_list = get_song_scope()
random.shuffle(song_list)
process_time = round(time.time() - start_time, 2)
print '--- song list created & shuffled. Time elapsed {} seconds ---'.format(process_time)
print '\n'


for song in song_list:
    try:
        gather_lyrics(song)
    except:
        pass
    
