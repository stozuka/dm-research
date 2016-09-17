# -*- coding: utf-8 -*-
from pymongo import MongoClient
import mojimoji
import keys

def connect_to_db():
    connect = MongoClient(keys.MongoIP, 27017)
    db = connect.research
    original_collection = db.all_tweets
    new_collection = db.opinionated_tweets
    return [original_collection, new_collection]

def conditions(doc):
    keywords = keys.OPINIONATED_KEYWORDS.split()
    for keyword in keywords:
        if keyword in doc['text']:
            return True
    return False

def extract_texts(docs, new_collection):
    for doc in docs:
        if conditions(doc):
            new_collection.insert_one(doc)

if __name__ == '__main__':
    original_collection, new_collection = connect_to_db()
    docs = original_collection.find()
    extract_texts(docs, new_collection)
