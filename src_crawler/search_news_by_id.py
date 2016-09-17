# -*- coding: utf-8 -*-
from twython import Twython
from twython import TwythonRateLimitError
from twython import TwythonAuthError
from twython import TwythonError
from warnings import warn
from datetime import datetime
from time import sleep
from pymongo import MongoClient
import keys

def authentification():
    APP_KEY = keys.APP_KEY
    APP_SECRET = keys.APP_SECRET
    OAUTH_TOKEN = keys.OAUTH_TOKEN
    OAUTH_TOKEN_SECRET = keys.OAUTH_TOKEN_SECRET
    api = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    return api

def get_tweets(screen_name=None, user_id=None, num=0, include_rts=False, since_id=730644442189680640):
    twitter = authentification()

    tweets = None
    while(tweets == None):
        try:
            if screen_name == None:
                tweets = twitter.get_user_timeline(user_id=user_id, count=200, trim_user=False, include_rts=include_rts, since_id=since_id)
            else:
                tweets = twitter.get_user_timeline(screen_name=screen_name, count=200, trim_user=False, include_rts=include_rts, since_id=since_id)
        except TwythonRateLimitError:
            warn("Fall asleep")
            sleep(300)
            pass
        except  TwythonAuthError:
            warn("Bad authentification")
            return []
        except TwythonError:
            warn("404 not found")
            return []

    totalTweets = tweets
    while len(tweets) >= 2:
        max_id = tweets[-1]["id"]
        try:
            if screen_name == None:
                tweets = twitter.get_user_timeline(user_id=user_id, max_id=max_id, count=200, trim_user=False, include_rts=include_rts, since_id=since_id)
            else:
                tweets = twitter.get_user_timeline(screen_name=screen_name, max_id=max_id, count=200, trim_user=False, include_rts=include_rts, since_id=since_id)
        except TwythonRateLimitError:
            print("Fall asleep")
            sleep(300)
            continue

        if len(tweets) > 1:
            totalTweets += tweets[1:]
        elif num > 0 and len(tweets) >= num :
            break

    if num == 0:
        return totalTweets
    else:
        return totalTweets[:num]

def save_into_mongo(data):
    connect = MongoClient(keys.MongoIP, 27017)
    db = connect.research
    tweetdata = db.original_testing_news
    try:
        tweetdata.insert(data)
    except Exception as e:
        print(e)
        pass

def get_news_account_ids():
    ids = []
    for line in open('news_account_list.txt', 'r'):
        id = line.split(',')[2].strip()
        ids.append(id)
    return ids

if __name__ == '__main__':
    # ID of the latest tweet in original_news collection.
    # 730644442189680640

    ids = get_news_account_ids()
    for id in ids:
        results = get_tweets(screen_name=None, user_id=id, since_id=730644442189680640)
        save_into_mongo(results)

    # # When use only one user_id
    # results = get_tweets(screen_name=None, user_id=204245399)
    # save_into_mongo(results)
