# -*- coding: utf-8 -*-
import sys
import glob


def get_files():
    base_path = '/home/sadayuki/Dropbox/Data-Mining-Research/'
    in_files = base_path + 'data_combined_results/new_approach_final/after_mean_2_first/std_600/mean1_1_8/mean2_1_7'
    out_file = base_path + 'data_stat_final/after_mean_2_first_emo_count'
    return in_files, out_file

def make_count_dict(in_file):
    result = {}
    with open(in_file, 'r') as f:
        for line in f:
            emos = line.strip().split('\t')[-1].split()
            emo_num = len(emos)
            result[emo_num] = result.get(emo_num, 0) + 1
    return result

def create_out_file(result, out_file):
    with open(out_file, 'w+') as f:
        total = 0
        for emo_num, count in result.items():
            f.write(str(emo_num) + ' emotion(s) ' + str(count) + '\n')
            total += count
        f.write('total ' + str(total))

def count_emo():
    in_file, out_file = get_files()
    result = make_count_dict(in_file)
    print(result)
    create_out_file(result, out_file)

if __name__ == '__main__':
    count_emo()
