# -*- coding: utf-8 -*-
from twython import Twython
from twython import TwythonRateLimitError
from pymongo import MongoClient
from datetime import datetime
import time
from warnings import warn
import re
import keys
import query

#>>>>>>>>>> Select one emotion >>>>>>>>>>
# EMOTION = "joy"
# EMOTION = "trust"
# EMOTION = "fear"
# EMOTION = "surprise"
# EMOTION = "sadness"
# EMOTION = "disgust"
# EMOTION = "anger"
EMOTION = "anticipation"
#<<<<<<<<<< Select one emotion <<<<<<<<<<

#>>>>>>>>>> Set since_id and max_id if needed >>>>>>>>>>
# If you don't want to set max_id or since_id, leave them None.
# since_id = 735062859088957442
since_id = None
max_id = None
# max_id = 726224831151112192 - 1
#<<<<<<<<<< Set since_id and max_id if needed >>>>>>>>>>

def create_query_str(words):
    result = []
    words = words.split()
    for word in words:
        word = "#" + word # This is a multibite hash. You can change ＃(multibite) to #(singlebite) if needed.
        result.append(word)
    result = " OR ".join(result)
    return result

def api_authentification():
    APP_KEY = keys.APP_KEY
    APP_SECRET = keys.APP_SECRET
    OAUTH_TOKEN = keys.OAUTH_TOKEN
    OAUTH_TOKEN_SECRET = keys.OAUTH_TOKEN_SECRET
    api = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    return api

def crawl_tweets(api, query, is_first_req, req_num, max_id=None, since_id=None):
    print("############### crawl_tweets: Request number " + str(req_num) + " ############### ", str(datetime.now()))
    try:
        if is_first_req and max_id == None:
            print("Came to the first condition for crawling tweets.")
            results = api.search(q=query, count=100, lang="ja", include_entities='true')
        elif since_id != None:
            print("Came to the second condition for crawling tweets.")
            results = api.search(q=query, count=100, lang="ja", max_id=max_id, since_id=since_id, include_entities='true')
        else: # When since_id == None, comes here
            print("Came to the third condition for crawling tweets.")
            results = api.search(q=query, count=100, lang="ja", max_id=max_id, include_entities='true')

        # If there is no more tweet, return None to stop this program.
        if results['statuses']: # Check if there is tweet in results.
            return results
        else: # results['status'] != True. That means there is no more tweet.
            print("No more tweet. Return None to the main function.")
            return None
    # Catch the "too many request" (API limit) exception.
    except TwythonRateLimitError:
        warn("Hit the API rate limit. Sleep.")
        # time.sleep(930)
        # return True
    # Catch the exceptions other than API limit.
    except Exception as err:
        print('Error when getting results. Return None to the main function.')
        print(err, "(" + str(datetime.now()) + ")")
        return None

# To add the data of insertion into the database.
def add_insert_date(result):
    result["inserted_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return result

def save_into_db(results, max_id):
    collection = connect_to_db()
    # Assign max_id to last_tweet_id to avoid last_tweet_id will be empty when all the tweets are rejected by the conditions set in check_conditions.
    last_tweet_id = max_id
    for result in results['statuses']:
        is_conditions_ok = check_conditions(result)
        if is_conditions_ok:
            try:
                result = add_insert_date(result)
                # Insert the data into the collection.
                collection.insert(result)
                # Show text and its ID on terminal.
                print(result['text'])
                print("Tweet ID:", result['id_str'])
                print("--------------------------------------------------")
            except Exception as err:
                print('Exception when saving data into database.')
                print(err, "(" + str(datetime.now()) + ")")
                print("Sleep 3 mins, then restart.")
                time.sleep(180)
                pass
        else:
            pass
        # Please check Twitter's developer website to know why -1 is added.
        last_tweet_id = int(result["id_str"]) - 1
    return str(last_tweet_id)

def check_conditions(result):
    # To remove non-official retweet.
    contain_RT = re.search(r'RT', result["text"])
    # Remove tweet with URL to the other website while URL to media such as photo and video is allowed.
    contain_url_except_media_url = result["entities"]["urls"]
    is_retweeted = result["retweeted"]
    retweet_count = result["retweet_count"]
    if not contain_RT and not contain_url_except_media_url and not is_retweeted and not is_retweeted:
        return True
    else:
        return False

def connect_to_db():
    connect = MongoClient(keys.MongoIP, 27017)
    db = connect.research
    collection = db["extra_" + EMOTION]
    return collection

# Twitter API allows 180 requests for 15 mins.
# You can change the number below.
def check_request_num(req_num):
    if req_num == 175:
        fall_asleep()
        req_num = 0
    else:
        req_num += 1
    return req_num

# We can start crawling after 15 mins when hitting the rate limit.
def fall_asleep():
    print('The number of request has reached 175. Sleep.')
    print("(" + str(datetime.now()) + ")")
    time.sleep(930)

if __name__ == '__main__':
    if EMOTION == "joy":
        query = create_query_str(query.JOY)
    elif EMOTION == "trust":
        query = create_query_str(query.TRUST)
    elif EMOTION == "fear":
        query = create_query_str(query.FEAR)
    elif EMOTION == "surprise":
        query = create_query_str(query.SURPRISE)
    elif EMOTION == "sadness":
        query = create_query_str(query.SADNESS)
    elif EMOTION == "disgust":
        query = create_query_str(query.DISGUST)
    elif EMOTION == "anger":
        query = create_query_str(query.ANGER)
    elif EMOTION == "anticipation":
        query = create_query_str(query.ANTICIPATION)

    req_num = 1
    is_first_req = True # This is used in crawl_tweets function.
    api = api_authentification()

    while True:
        results = crawl_tweets(api, query, is_first_req, req_num, max_id, since_id)
        if is_first_req:
            is_first_req = False
        if results:
            max_id = save_into_db(results, max_id)
            req_num = check_request_num(req_num)
        else:
            print('None was returned from the function to get data. Break.')
            break
