# -*- coding: utf-8 -*-
from pymongo import MongoClient
import keys

def connect_to_db(EMOTION):
    connect = MongoClient(keys.MongoIP, 27017)
    db = connect.research
    collection = db[EMOTION + "_tweets"]
    return collection

def rm_dup_tweets(docs):
    texts_and_ids = {}
    for doc in docs:
        texts_and_ids[doc['text']] = doc['id_str']
    return texts_and_ids

# ATTENTION: Pass one emotion as a command line argument
# 'joy', 'trust', 'fear', 'surprise', 'sadness', 'disgust', 'anger', 'anticipation', 'news', 'opinionated', 'testing_news'
if __name__ == '__main__':
    EMOTION = sys.argv[1]
    collection = connect_to_db(EMOTION)
    docs = collection.find()
    texts_and_ids = rm_dup_tweets(docs)
    for text, id in texts_and_ids.items():
        text = " ".join(text.split())
        print(text + "\t" + id)
