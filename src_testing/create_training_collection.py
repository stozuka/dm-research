# -*- coding: utf-8 -*-
import os
from pymongo import MongoClient
import keys

#>>>>>>>>>> Select one emotion >>>>>>>>>>
# EMOTION = 'joy'
# EMOTION = 'trust'
# EMOTION = 'fear'
# EMOTION = 'surprise'
# EMOTION = 'sadness'
# EMOTION = 'disgust'
# EMOTION = 'anger'
EMOTION = 'anticipation'
#<<<<<<<<<< Select one emotion <<<<<<<<<<

def get_list_to_be_rejected(file):
    id_list = []

    for line in file:
        text_id = line.strip().split("\t")
        id_list.append(text_id[1])

    return id_list

def connect_to_db():
    connect = MongoClient(keys.MongoIP, 27017)
    db = connect.research

    original_collection = db[EMOTION + "_tweets"]
    training_collection = db["training_" + EMOTION]

    return [original_collection, training_collection]

def insert_doc_to_training_collection(id_list):
    original_collection, training_collection = connect_to_db()

    for doc in original_collection.find():
        if doc["id_str"] not in id_list:
            training_collection.insert_one(doc)

if __name__ == '__main__':
    file_name = EMOTION + "_random.txt"
    path_name = os.getcwd() + "/50tweets/random_tweets_final/" + file_name

    with open(path_name, mode="r") as file:
        id_list = get_list_to_be_rejected(file)
        insert_doc_to_training_collection(id_list)
