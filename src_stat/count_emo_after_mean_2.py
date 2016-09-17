# -*- coding: utf-8 -*-
import sys
import glob


def get_files():
    base_path = '/home/sadayuki/Dropbox/Data-Mining-Research/'
    in_files = base_path + 'data_combined_results/new_approach_final/after_mean_2_first/std_600/mean1_1_8/mean2_1_7'
    out_file  = base_path + 'data_stat_final/emo_left_after_mean_2_first'
    return in_files, out_file

def count_emo(in_f):
    sum = 0
    for line in in_f:
        emos = line.strip().split('\t')[-1].split(' ')
        sum += len(emos)
    return sum

def create_out_file(number, out_f):
    out_f.write('emos left after_mean_2 ' + str(number))

def count_emo_after_news():
    in_file, out_file = get_files()
    number = 0

    with open(in_file, 'r') as in_f:
        number = count_emo(in_f)

    with open(out_file, 'w+') as out_f:
        create_out_file(number, out_f)

def get_after_mean_count(mean):
    count_file = '/home/sadayuki/Dropbox/Data-Mining-Research/'\
                 'data_stat/after_mean_emo_count'
    with open(count_file, 'r') as f:
        for line in f:
            line_list = line.strip().split()
            if mean == float(line_list[0]):
                return int(line_list[1])

if __name__ == '__main__':
    count_emo_after_news()
