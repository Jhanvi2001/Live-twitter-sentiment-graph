# -*- coding: utf-8 -*-
"""
Created on Sat Sep 11 10:08:07 2021

@author: sjhan
"""
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import sqlite3
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from unidecode import unidecode
import time

analyzer = SentimentIntensityAnalyzer()

conn = sqlite3.connect('exp1.db')
c = conn.cursor()

def create_table():
    try:
        c.execute("CREATE TABLE IF NOT EXISTS sentiment(unix REAL, tweet TEXT, sentiment REAL)")
        c.execute("CREATE INDEX unix ON sentiment(unix)")
        c.execute("CREATE INDEX tweet ON sentiment(tweet)")
        c.execute("CREATE INDEX sentiment ON sentiment(sentiment)")
        conn.commit()
    except Exception as e:
        print(str(e))
create_table()

#consumer key, consumer secret, access token, access secret.
ckey="wwoXP6iLVHXI5za08zudK90xF"
csecret="Aq6lajJ56O0neFsWJT4aR99XCOJ5vs14EmnrAhKjGEEfQ4kWCA"
atoken="1433817013793607680-4uNjHfglzFDvm8xft5zqMom4GXKLux"
asecret="ptVGkS3QnOxIu3bY3RrEU2FDuOLj3zRB0A3h2x1LEVvm3"

class listener(StreamListener):

    def on_data(self, data):
        try:
            data = json.loads(data)
            tweet = unidecode(data['text'])
            time_ms = data['timestamp_ms']
            vs = analyzer.polarity_scores(tweet)
            sentiment = vs['compound']
            print(time_ms, tweet, sentiment)
            c.execute("INSERT INTO sentiment (unix, tweet, sentiment) VALUES (?, ?, ?)",
                  (time_ms, tweet, sentiment))
            conn.commit()

        except KeyError as e:
            print(str(e))
        return(True)

    def on_error(self, status):
        print(status)


while True:

    try:
        auth = OAuthHandler(ckey, csecret)
        auth.set_access_token(atoken, asecret)
        twitterStream = Stream(auth, listener())
        twitterStream.filter(track=["a","e","i","o","u"])
    except Exception as e:
        print(str(e))
        time.sleep(5)

