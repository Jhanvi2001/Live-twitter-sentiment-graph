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
from textblob import TextBlob
from unidecode import unidecode
import time


#create database to store all the  tweets and their sentiments
conn = sqlite3.connect('database_name.db')
c = conn.cursor()

#table with certain components
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

#here build your own app and get consumer key and others
#consumer key, consumer secret, access token, access secret.
ckey=""
csecret=""
atoken=""
asecret=""

class listener(StreamListener):

    def on_data(self, data):
        try:
            data = json.loads(data)
            tweet = unidecode(data['text'])
            time_ms = data['timestamp_ms']
            analysis=TextBlob(tweet)
            
            sentiment = analysis.sentiment.polarity
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
        
        #filter out the tweets with particular word or lists
        twitterStream.filter(track=["a","e","i","o","u"])
    except Exception as e:
        print(str(e))
        time.sleep(5)

