# -*- coding: utf-8 -*-
from pymongo import MongoClient
import os
import sys
import numpy
import keys

if __name__ == '__main__':
    EMOTION   = sys.argv[1]
    base_path = "/home/sadayuki/Dropbox/Data-Mining-Research/"
    in_file   = base_path + "data_testing/original_after_rm_dup/original_" + EMOTION
    out_file  = base_path + "data_testing/random_200/random_200_" + EMOTION

    texts_ids = []
    with open(in_file, mode="r") as in_file, open(out_file, mode="w+") as out_file:
        for line in in_file:
            line = line.strip()
            text_id = line.split("\t")
            texts_ids.append(text_id)

        size = len(texts_ids)
        rand_array = numpy.random.randint(0, size, 200)

        for i in rand_array:
            text = texts_ids[i][0]
            id = texts_ids[i][1]
            out_file.write(text + '\t' + id + '\n')
