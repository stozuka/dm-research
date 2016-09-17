# -*- coding: utf-8 -*-
from pymongo import MongoClient
import re
import mojimoji
import keys

def connect_to_db():
    connect = MongoClient(keys.MongoIP, 27017)
    db = connect.research
    collection = db.news_tweets
    return collection

def separate_url_and_hashtag(text):
    text = text.replace("。http", "。 http")
    text = text.replace("。#", "。 #")
    text = text.replace("、#", "、 #")
    text = text.replace("・#", "・ #")
    return text

def is_starts_with_hashtag(item):
    pattern = r"\#"
    return re.match(pattern, item)

def is_starts_with_url(item):
    pattern = r"http"
    return re.match(pattern, item)

def is_starts_with_at(item):
    pattern = r"@"
    return re.match(pattern, item)

def is_starts_with_text(item):
    if is_starts_with_hashtag(item) or is_starts_with_at(item) or is_starts_with_url(item):
        return False
    else:
        return True

def segmentation(text):
    segmented_text = []
    for item in text:
        if is_starts_with_text(item):
            chars = list(item)
            for char in chars:
                segmented_text.append(char)
        else: # startswith #, @, or http
            segmented_text.append(item)
    return segmented_text

def combine_non_ja_chars(word_list):
    result = []
    non_japanese_str = ""
    pattern = r'[一-龠ぁ-んァ-ヶ【】「」]'

    for char in word_list:
        if is_starts_with_text(char):
            if re.match(pattern, char): # If Japanese character
                if non_japanese_str != "":
                    result.append(non_japanese_str)
                    non_japanese_str = ""
                result.append(char)
            else: # If not Japanese character
                non_japanese_str = non_japanese_str + char
        else: # If start with #, @ or http.
            if non_japanese_str != "":
                result.append(non_japanese_str)
                non_japanese_str = ""
            result.append(char)

    if not non_japanese_str == "":
        result.append(non_japanese_str)

    return result

def preprocessing(docs):
    processed_texts = []
    for doc in docs:
        # text is a string
        text = doc['text']
        text = mojimoji.zen_to_han(text, kana=False)
        text = separate_url_and_hashtag(text)
        # word_list is a list
        word_list = text.split()
        word_list = segmentation(word_list)
        word_list = combine_non_ja_chars(word_list)
        processed_texts.append(word_list)
    return processed_texts

if __name__ == '__main__':
    collection = connect_to_db()
    # docs = collection.find().limit(1000)
    docs = collection.find()
    processed_texts = preprocessing(docs)
    for processed_text in processed_texts:
        print(" ".join(processed_text))
