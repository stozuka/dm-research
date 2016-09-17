# -*- coding: utf-8 -*-
import os
import sys
from pymongo import MongoClient
import keys

# ATTENTION: Pass one emotion as a command line argument
# 'joy', 'trust', 'fear', 'surprise', 'sadness', 'disgust', 'anger', 'anticipation', 'news', 'opinionated', 'testing_news'
if __name__ == '__main__':
    EMOTION   = sys.argv[1]
    base_path = "/home/sadayuki/Dropbox/Data-Mining-Research/"
    in_file   = base_path + "/data_original/rm_some_hashtags/reduced_" + EMOTION
    out_file  = base_path + "/data_testing/original_after_rm_dup/original_" + EMOTION

    with open(in_file, mode="r") as in_file, open(out_file, mode="w+") as out_file:
        texts_ids = {}

        for line in in_file:
            line = line.strip()
            temp = line.split('\t') # idx 0 for text, idx 1 for id
            texts_ids[temp[0]] = temp[1]

        for key, value in texts_ids.items():
            out_file.write(key + '\t' + value + '\n')
