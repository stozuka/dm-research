# -*- coding: utf-8 -*-

if __name__ == '__main__':
    base_path = "/home/sadayuki/Dropbox/Data-Mining-Research/"
    in_file   = base_path + "data_original/original_tweets/original_testing_news"
    out_file  = base_path + "data_evaluation/reduced_news/original/all"

    with open(in_file, 'r') as in_f, open(out_file, 'w+') as out_f:
        for line in in_f:
            text = line.strip().split('\t')[0]
            out_f.write(text + '\n')
