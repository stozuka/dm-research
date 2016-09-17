# -*- coding: utf-8 -*-
from pymongo import MongoClient
import mojimoji
import keys

#>>>>>>>>>> Select one emotion >>>>>>>>>>
# EMOTION = 'joy'
EMOTION = 'trust'
# EMOTION = 'fear'
# EMOTION = 'surprise'
# EMOTION = 'sadness'
# EMOTION = 'disgust'
# EMOTION = 'anger'
# EMOTION = 'anticipation'
# EMOTION = 'news'
#<<<<<<<<<< Select one emotion <<<<<<<<<<

def connect_to_db():
    connect = MongoClient(keys.MongoIP, 27017)
    db = connect.research
    collection = db[EMOTION + "_tweets"]
    return collection

# def Conditions(doc):
#     if 'test' in doc['text']:
#         return True
#     else:
#         return False

    def extract_texts(docs):
    ret = []
    text_and_id = []
    for doc in docs:
        # if Conditions(doc):
        #     text = doc['text']
        #     id = doc['id_str']
        #     ret.append([text, id])
        text = doc['text']
        id = doc['id_str']
        ret.append([text, id])
    return ret

if __name__ == '__main__':
    collection = connect_to_db()
    # If setting limit, write like this
    # `collection.find().limit(1000)`.
    docs = collection.find()
    texts_and_ids = extract_texts(docs)

    num_of_docs = 1 # To count the number of documents printed.
    for text_and_id in texts_and_ids:
        print(num_of_docs)
        num_of_docs += 1
        print(text_and_id[0])
        print('Tweet ID:', text_and_id[1])
        print('-------------------------------------------')
