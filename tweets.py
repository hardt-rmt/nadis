import tweepy
import os

BEARER_TOKEN = os.getenv('BEARER_TOKEN')

class TweetStream(tweepy.StreamingClient):
    # Handle incoming tweets
    def on_tweet(self, tweet):
        print(f"New Tweet: {tweet.text}")

    # Callback for successful connection
    def on_connect(self):
        print("Connected to the Twitter stream.")

    # Handle errors if any
    def on_errors(self, status_code):
        print(f"Error occurred: {status_code}")
        return False  # Stop stream on errors

def data_load():
    # Set up the stream with a bearer token
    stream = TweetStream(bearer_token=BEARER_TOKEN)

    try:
        # Add rules for filtering tweets
        keywords = ['earthquake', 'flood', 'hurricane', 'tornado', 'tsunami']
        for keyword in keywords:
            stream.add_rules(tweepy.StreamRule(keyword)) 
        print("Rules added. Starting stream...")

        # Start streaming
        return stream.filter()
    except KeyboardInterrupt:
        print("Stream stopped.")
    finally:
        # Clean up rules when the stream ends
        rules = stream.get_rules().data
        if rules:
            rule_ids = [rule.id for rule in rules]
            stream.delete_rules(rule_ids)

