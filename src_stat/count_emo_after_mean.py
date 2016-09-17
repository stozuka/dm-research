# -*- coding: utf-8 -*-
import sys
import glob


def get_files():
    base_path = '/home/sadayuki/Dropbox/Data-Mining-Research/'
    in_files = glob.glob(
        base_path +
        'data_combined_results/new_approach_final/after_mean/*'
        )
    out_file  = base_path + 'data_stat_final/after_mean_emo_count'
    return in_files, out_file

def count_emo(in_f):
    sum = 0
    for line in in_f:
        emos = line.strip().split('\t')[-1].split(' ')
        # Because news is included, len(emos) - 1
        sum += len(emos) - 1
    return sum

def create_out_file(count_list, out_f):
    for rate, count in sorted(count_list, key=lambda x: x[0]):
        out_f.write(str(rate) + ' ' + '{0:>4}'.format(str(count)) + '\n')

def count_emo_after_mean():
    in_files, out_file = get_files()
    count_list = []

    for in_file in in_files:
        with open(in_file, 'r') as in_f:
            rate = float(in_file.split('/')[-1].replace('_', '.'))
            number = count_emo(in_f)
            count_list.append([rate, number])

    with open(out_file, 'w+') as out_f:
        create_out_file(count_list, out_f)

if __name__ == '__main__':
    count_emo_after_mean()
