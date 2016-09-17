# -*- coding: utf-8 -*-
from twython import Twython
from twython import TwythonStreamer
from pymongo import MongoClient
import re
import keys

# Twitter API information
APP_KEY = keys.APP_KEY
APP_SECRET = keys.APP_SECRET
OAUTH_TOKEN = keys.OAUTH_TOKEN
OAUTH_TOKEN_SECRET = keys.OAUTH_TOKEN_SECRET
api = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

# Connect to mongo DB
connect = MongoClient(keys.MongoIP, 27017)
db = connect.research
collection = db.validation

class MyStreamer(TwythonStreamer):
    def on_success(self, data):
        if 'text' in data:
            # contain_RT = re.search(r'RT', data['text'])
            # contain_url_except_media_url = data["entities"]["urls"]
            # is_retweeted = data['retweeted']
            # retweet_count = data['retweet_count']
            # user_lang = data["user"]["lang"]
            #
            # if not contain_url_except_media_url and not is_retweeted and retweet_count == 0 and user_lang == "ja":
                try:
                    collection.insert(data)
                    print(data['text'])
                    print('-------------------------------------')
                except Exception as err:
                    print('Error when trying to insert data into Mongo:', err)

    def on_error(self, status_code, data):
        print("Error.Status_code:", status_code)

# Start crawling
stream = MyStreamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
stream.statuses.filter(track="happy")
# stream.statuses.filter(track=[])

