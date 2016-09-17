# -*- coding: utf-8 -*-
from pymongo import MongoClient
import sys
import keys

def get_hashtags(EMOTION):
    hashtags_to_be_rejected = {
        'joy':['#成功', '#面白い', '#爆笑'],
        'trust':['#ポジティブ', '#前向き', '#頑張るぞ'],
        'fear':['#怖い', '#こわい', '#怖い', '#コワイ'],
        'surprise':['#サプライズ', '#まじか'],
        'sadness':['#ぼっち'],
        'disgust':['#暇','#ひま','#ヒマ','#最低','#面倒','#面倒くさい','#めんどくさい','#めんどう', '#毒舌'],
        'anger':['#イライラ', '#怒り'],
        'anticipation':['#楽しみ', '#がんばれ', '#頑張れ', '#頑張って', '#頑張ってね']
    }
    return hashtags_to_be_rejected[EMOTION]

def condition(line, EMOTION):
    hashtags = get_hashtags(EMOTION)
    for hashtag in hashtags:
        if hashtag in line:
            return False
    return True

if __name__ == '__main__':
    EMOTION = sys.argv[1]
    data_dir = "/home/sadayuki/Dropbox/Data-Mining-Research/data_original/"
    in_file = data_dir + "/original_tweets/original_" + EMOTION
    out_file = data_dir + "/rm_some_hashtags/reduced_" + EMOTION

    with open(in_file, mode="r") as in_file, open(out_file, mode="w+") as out_file:
        for line in in_file:
            if condition(line, EMOTION):
                out_file.write(line)
