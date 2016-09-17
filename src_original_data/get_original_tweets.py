# -*- coding: utf-8 -*-
from pymongo import MongoClient
import sys
import keys

def connect_to_db(EMOTION):
    connect = MongoClient(keys.MongoIP, 27017)
    db = connect.research
    collection = db["original_" + EMOTION]
    return collection

def extract_texts(docs):
    ret = []
    text_and_id = []
    for doc in docs:
        text = " ".join(doc['text'].strip().split()).replace("＃", "#")
        id = doc['id_str'].strip()
        ret.append([text, id])
    return ret

# ATTENTION: Pass one emotion as a command line argument
# 'joy', 'trust', 'fear', 'surprise', 'sadness', 'disgust', 'anger', 'anticipation', 'news', 'opinionated', 'testing_news'
if __name__ == '__main__':
    EMOTION = sys.argv[1]
    collection = connect_to_db(EMOTION)
    docs = collection.find()
    texts_and_ids = extract_texts(docs)

    out_file = "/home/sadayuki/Dropbox/Data-Mining-Research/data_original/original_tweets/original_" + EMOTION

    with open(out_file, mode="w+") as out_file:
        for text_and_id in texts_and_ids:
            out_file.write(text_and_id[0] + "\t" + text_and_id[1] + "\n")
