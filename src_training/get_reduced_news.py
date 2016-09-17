# -*- coding: utf-8 -*-
import os
import sys
import numpy

def get_text(in_file):
    result = []
    with open(in_file, mode='r') as i_f:
        for line in i_f:
            text = line.strip().split('\t')[0]
            result.append(text)
    return result

def write_file(text, out_file):
    text_array_size = len(text)
    rand_int = numpy.random.randint(0, text_array_size, num_of_tweets)
    with open(out_file, 'w+') as o_f:
        for i in rand_int:
            o_f.write(text[i] + '\n')

def create_file(num_of_tweets, in_file, out_file):
    text = get_text(in_file)
    # print(text)
    write_file(text, out_file)

if __name__ == '__main__':
    num_of_tweets = 5000
    base_path = '/home/sadayuki/Dropbox/Data-Mining-Research/'
    in_file   = base_path + 'data_original/original_tweets/original_testing_news'
    out_file  = base_path + 'data_evaluation/reduced_news/original/' + str(num_of_tweets)

    create_file(num_of_tweets, in_file, out_file)
