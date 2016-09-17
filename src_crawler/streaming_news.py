# -*- coding: utf-8 -*-
from twython import Twython
from twython import TwythonStreamer
from pymongo import MongoClient
from datetime import datetime
import re
import keys
import query

# Twitter API information
APP_KEY = keys.APP_KEY
APP_SECRET = keys.APP_SECRET
OAUTH_TOKEN = keys.OAUTH_TOKEN
OAUTH_TOKEN_SECRET = keys.OAUTH_TOKEN_SECRET
api = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

# Connect to mongo DB
connect = MongoClient(keys.MongoIP, 27017)
db = connect.research
tweetdata = db.news_tweets

class MyStreamer(TwythonStreamer):
    def on_success(self, data):
        try:
            if 'text' in data:
                # Remove unofficial retweets
                contain_RT = re.search(r'RT', data['text'])
                # Remove tweets containing @. To remove non-news tweets mentioning news accounts.
                contain_at = re.search(r'@', data['text'])
                # Remove official retweets, but it seems this always return false and useless
                is_retweeted = data['retweeted']
                # Remove official retweets. Because above data['retweeted'] looks useless, I want to make sure I can remove official retweet by adding this.
                retweet_count_is_zero = data['retweet_count'] == 0

                if not contain_RT and not contain_at and not is_retweeted and retweet_count_is_zero:
                    try:
                        tweetdata.insert(data) # Insert to mongo db
                        print(data['text']) # Print to terminal
                    except Exception as err:
                        print(err, "(" + str(datetime.now()) + ")")
        except Exception as err:
            print('Exception happened. Sleep 5 mins.', err)
            time.sleep(300)

    def on_error(self, status_code, data):
        print(status_code)

# Start crawling
stream = MyStreamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
stream.statuses.filter(follow=query.ID_LIST)
