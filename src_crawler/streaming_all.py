#!/usr/local/bin/python
# -*- coding:utf-8 -*-

# Important Please use python2 to run this code

import json, urllib2, oauth2 as oauth
from pymongo import MongoClient
import time
import keys

# Set keys
consumer = oauth.Consumer(key = keys.APP_KEY, secret = keys.APP_SECRET)
token = oauth.Token(key = keys.OAUTH_TOKEN, secret = keys.OAUTH_TOKEN_SECRET)

# Oauth authentification and connect to mongo DB
connect = MongoClient(keys.MongoIP, 27017)
db = connect.research
# collection = db.all_tweets
collection = db.validation_tweets

url = 'https://stream.twitter.com/1.1/statuses/sample.json'

request = oauth.Request.from_consumer_and_token(consumer, token, http_url=url)
request.sign_request(oauth.SignatureMethod_HMAC_SHA1(), consumer, token)

count = 1;
while True:
    try:
        res = urllib2.urlopen(request.to_url())
    except Exception as err:
        print('Exception when crawling tweets.', err)
        break

    try:
        for r in res:
            data = json.loads(r)
            try:
                if data['user']['lang'] == 'ja' and data['retweet_count'] is 0:
                    collection.insert(data)
                    print "count:", count, "Tweet ID:", data['id']
                    # print data['text']
                    count += 1
            except Exception as err:
                # print("Exception: ", err)
                pass
    except Exception as err:
        print('Exception happened when processing data.', err)
        # time.sleep(3)
        # pass
