# -*- coding: utf-8 -*-

from pymongo import MongoClient
import keys

cliant = MongoClient(keys.MongoIP, 27017)
db = cliant.research
old_collection = db.anger_tweets
new_collection = db.anger_no_dup

uniq = []

for doc in old_collection.find():
    if doc['id'] not in uniq:
        uniq.append(doc['id'])
        new_collection.insert_one(doc)
    else:
        pass
