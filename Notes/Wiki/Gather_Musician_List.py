# The following script will open a file made of url's to wikipedia articles that contain a comprehensive list of
# Hip Hop artists and groups, and enter the names of those Musicaians into a MongoDB database

# Import packages needed to webscrape wikipedia and capture the time
import requests, time, datetime
from Wiki_Urls import Wiki_Urls
from pymongo import MongoClient
from bs4 import BeautifulSoup

# Declare class to get wiki urls
wiki = WikiUrls()

# get html from rap artist and group urls
artist_html = requests.get(wiki.artists_url).content
group_html = requests.get(wiki.groups_url).content

# use beautiful soup to parse html from content
artist_soup = BeautifulSoup(artist_html, 'html.parser')
group_soup = BeautifulSoup(group_html, 'html.parser')

# find the correct html element to pull out the artist and group names
artist_soup_select = artist_soup.select('.div-col.columns.column-width ul li a')
group_soup_select = group_soup.select('.div-col.columns.column-count.column-count-3 ul li a')

# Create a list from the soup select text
artist_list = [artist.text for artist in artist_soup_select]
group_list = [group.text for group in group_soup_select]

# Clean some bad html data out of lists
artist_list = [artist for artist in artist_list if artist.find('[') != 0]
group_list = [group for group in group_list if group.find('[') != 0]

# Create a MongoDB Client
client = MongoClient()

# Connect to The Mack App DB
db = client['mack']

# Connect to Musician table
musician_table = db['musician']

# Add artists to Musician table
for artist in artist_list:
    date_added = datetime.datetime.now().strftime("%Y-%m-%d")
    musician_table.insert({'musician_name': artist, 'date_added': date_added, 'musician_type': 'artist'})

# Add groups to Musician table
for group in group_list:
    date_added = datetime.datetime.now().strftime("%Y-%m-%d")
    musician_table.insert({'musician_name': group, 'date_added': date_added, 'musician_type': 'group'})
