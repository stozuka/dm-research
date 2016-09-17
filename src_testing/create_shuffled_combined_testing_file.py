# -*- coding: utf-8 -*-
import random

def create_output_file(out_file, texts_ids):
    with open(out_file, mode='w+') as out_file:
        for text_id in texts_ids:
            line = '\t'.join(text_id) + '\n'
            out_file.write(line)

def create_in_file_list(in_file):
    texts_ids = []
    with open(in_file, mode='r') as in_file:
        for line in in_file:
            line = line.strip()
            text_id = line.split('\t')
            texts_ids.append(text_id)
    return texts_ids

def create_shuffled_file(in_file, out_file):
    texts_ids = create_in_file_list(in_file)
    for i in range(10): # I think 10 times is enough.
        random.shuffle(texts_ids)
    create_output_file(out_file, texts_ids)

if __name__ == '__main__':
    base_path = '/home/sadayuki/Dropbox/Data-Mining-Research/data_testing/manual_classification/'
    in_file = base_path + 'combined_testing_data.txt'
    out_file  = base_path + 'shuffled_combined_testing_data.txt'
    create_shuffled_file(in_file, out_file)
