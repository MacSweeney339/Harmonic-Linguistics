# Harmonic Linguistics
This project is the result of a Data Science immersion program with Galvanize. For my capstone project I decided to analyze the content of hip hop lyrics through the lens of a Data Scientist. This project exists to help you discover which artists rap about similar subjects and explore their music in new and meaningful ways.

# Motivation
Harmonic Linguistics aims to provide engaging products that help people explore and discover the rich genre of Hip Hop. As a way to thank the community that has produced such an amazing culture, I'd like to use this project as a fundraising platform to support African American students in STEM and Creative Arts programs.

# Approach
To accomplish my project I chose the following approach
* Collect the lyrics to as many hip hop songs as possible
* Extract features from those lyrics
* Use those extracted features to model the similarities between the artists and create "clusters"
* Design an engaging web application to visualize these artist clusters

# Data Collection
I've been using Spotify and Rap Genius for at least 5 years now, so I decided to use their API's for my project. I used Spotify's API to gather the list of songs for the scope of my project, and Rap Genius to collect the lyrics to those songs. I discovered I already needed to know which musicians I wanted songs for before I could use either of these API's so I can up with a way to collect a list of musicians.

## Wikipedia
I found a relatively comprehensive list of [artists](https://en.wikipedia.org/wiki/List_of_hip_hop_musicians) and [groups](https://en.wikipedia.org/wiki/List_of_hip_hop_groups) on Wikipedia. Using artist_group_wiki.txt, Wiki_Urls.py, and Gather_Wiki_Musicians.py I scraped wikipedia to create a list of musicians and entered those musicians into MongoDB.

## Spotify
Once I had my musicians stored in MongoDB, I registered an application with Spotify in order to use their API. I stored my key and credentials in the SpotifyKey file, used a Spotify_Credentials.py class to use those credentials, and collected my Spotify data using Gather_Spotify_Data.py.

**side note:** At first, I started writing my own Spotipy client class but then I found a light weight Python library for the Spotify Web API was already written called [Spotipy](https://github.com/plamere/spotipy). I highly recommend for anyone looking to develop Spotify apps using python.

## Genius
With a list of artists and songs in MongoDB, I had what I needed to get song lyrics from Rap Genius. I registered an application with Genius, stored my credentials in GeniusKey, and wrote a class to access those credentials called GeniusKey.py. I then collected lyrics using Gather_Genius_Data.py.

**side note:** I used instructions I found in this [Getting Song Lyrics from Genius’s API + Scraping] (https://bigishdata.com/2016/09/27/getting-song-lyrics-from-geniuss-api-scraping/) blog post from bigishdata.com as the a reference to build Gather_Genius_Data.py.

# Feature Extraction
To extract features from the songs lyrics, I employed some basic natural language processing techniques. In future iterations, I'll look to combine additional features from Spotify metadata into the project.

## Natural Language Processing
I wrote a custom tokenize function to process the song lyric text to handle text that wasn't really "lyrics."" I used nltk english stop words and Word Net Lemmatizer for additional text processing. I chose to go with a tfidf vectorizer to extract feature weights for the tokenized song lyrics.

## Dimensionality Reduction
For my first model, I chose to go with the dimensionality reduction technique Non-Negative Matrix Factorization (NMF). Applying NMF generated a matrix containing artists and "hidden features" we can call "Topics" contained within the lyrics, along with values indicating the strength of the relationship between the two. NMF also produced a matrix of those same "Topics" and the strength of their relationship with individual words.

For the first version of the model, I took the most strongly correlated topic for each artist and assigned that topic as the artist's "category."

# Considerations for Future Iterations
### Modeling
The modeling portion of this MVP is thin, and I've made notes on additional methods to explore in future iterations which include principle component analysis, latent semantic analysis, cosine similarity, and building a recommender.

### Language
I discovered through the first iteration that the categories created using NMF are largely revealing language differences between artists. I hadn't considered the variety of languages spoken by the artists in my dataset. To address this, I'll use language detection tools to split the artists and songs into categories by dominant language. Then I can process and categorize artists by topic within those languages.

### Domain Specific Stop-Words
I found some hip hop domain specific stop words became important to hidden features in the categories. Future iterations may involve generating a custom list of hip hop stop words to remove from the corpus.

### Text Cleaning
A significant number of typos and 'non-lyric' text appeared in the tokenized text. Future iterations will involve more rigorous text cleaning. By not fixing typos, I'd be weary that common typos by someone responsible for documenting lyrics could leak into the feature extraction process.

### Additional Features
There is an opportunity to explore more features and their relationship to those already generated. Examples would be.
* Spotify metadata i.e. 'danceability', 'speechiness', 'energy', 'acousticness', etc.
* Additional features extracted from the lyrics i.e. 'vocabulary size', 'rhyme scheme complexity', 'rhyme type frequencies', 'metaphor usage' etc.

# Visualization
## Inspiration
You can find the visual inspiration for the end product of this project in the Visualization_Examples.ipynb jupyter notebook file. Below are screenshots of the current version of the website.

## Website
To create an engaging site for Harmonic Linguistics, I used Flask, D3, and a Bootstrap template. The integration of these pieces has yet to be completed.

### Home
![website_1](https://github.com/MacSweeney339/Harmonic-Linguistics/blob/master/img/Website_1.png)
### About
![website_2](https://github.com/MacSweeney339/Harmonic-Linguistics/blob/master/img/Website_2.png)
### Artist Information
In this area of the app, you'll find information about artists and links to Spotify to listen to their music.
![website_3](https://github.com/MacSweeney339/Harmonic-Linguistics/blob/master/img/Website_3.png)
### Artist Clusters
In this area of the app, you'll be able to explore the clusters of artists. When clicking on a particular circle, the information about that artist appears in the artist information page above. The size of the artist's circle correlates to that artists popularity on Spotify.
![website_4](https://github.com/MacSweeney339/Harmonic-Linguistics/blob/master/img/Website_4.png)
![website_5](https://github.com/MacSweeney339/Harmonic-Linguistics/blob/master/img/Website_5.png)
The image below is a sketch of what the artists circles should eventually look like.
![clusters](https://github.com/MacSweeney339/Harmonic-Linguistics/blob/master/img/Clusters.png)
### Mission & Contact
![website_6](https://github.com/MacSweeney339/Harmonic-Linguistics/blob/master/img/Website_6.png)
