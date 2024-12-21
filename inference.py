from transformers import pipeline
import tweets
import pandas as pd
from preprocessor import preprocess_text
import spacy
from geopy.geocoders import Nominatim

'''
Due to cost I will not be streaming the tweets
'''
# tweet_data = tweets.data_load()

tweet_data = pd.read_csv('tweets.csv')
tweets = tweet_data['text'].values

classifier = pipeline('text-classification', model='./disaster_model')

# Extract disaster tweets from the data
def getDisasterTweets():
    disaster_tweets = []
    for tweet in tweets:
        clean_tweet = preprocess_text(tweet)
        result = classifier(clean_tweet)
        if result[0]['label'] == '1':
            disaster_tweets.append(clean_tweet)
    return disaster_tweets

# Extract locations from tweets
def getDisasterLocations():
    npl = spacy.load('en_core_web_sm')
    disaster_locations = []
    disaster_tweets = getDisasterTweets()
    for tweet in disaster_tweets:
        # Process the tweet
        doc = npl(tweet)
        # Extract location entities
        locations = [ent.text for ent in doc.ents if ent.label_ in ['GPE', 'LOC']]
        disaster_locations.append(locations[0])
    return disaster_locations

# Convert extracted locations into coordinates
def getDisasterCoordinates():
    disaster_coordinates = []
    disaster_locations = getDisasterLocations()
    geolocator = Nominatim(user_agent="disaster_app")
    for location in disaster_locations:
        coordinates = geolocator.geocode(location)
        disaster_coordinates.append(coordinates)
    return disaster_coordinates

# Perform sentiment analysis
def getSentiment():
    # Load sentiment analysis pipeline
    sentiment_analyzer = pipeline('sentiment-analysis')
    tweets_sentiment = []
    disaster_tweets = getDisasterTweets()
    for tweet in disaster_tweets:
        result = sentiment_analyzer(tweet)
        tweets_sentiment.append(tweet)
    return tweets_sentiment

# Get tweet severity
def detectSeverity(text):
    severe_keywords = ['massive', 'catastrophic', 'devastation', 'fatalities']
    moderate_keywords = ['significant', 'moderate', 'evacuations']
    mild_keywords = ['small', 'minor', 'tremor']
    tweets_severity = []
    disaster_tweets = getDisasterTweets()
    for tweet in disaster_tweets:
        tweet_lower = tweet.lower()
        severity = ''
        if any(word in tweet_lower for word in severe_keywords):
            severity = 'Severe'
        elif any(word in tweet_lower for word in moderate_keywords):
            severity = "Moderate"
        elif any(word in tweet_lower for word in mild_keywords):
            severity = "Mild"
        else:
            severity = "Unknown"
        tweets_severity.append(severity)
    return tweets_severity

