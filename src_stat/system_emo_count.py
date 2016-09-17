# -*- coding: utf-8 -*-
import sys


def get_files():
    base_path = '/home/sadayuki/Dropbox/Data-Mining-Research/'
    in_file = base_path + 'data_combined_results/rm_none/system_sentiment_trigram'
    out_file  = base_path + 'data_stat/system_emo_count_trigram'
    return in_file, out_file

def get_emo_count(emos, emo_count):
    result = emo_count
    for emo in emos:
        result[emo] = result.get(emo, 0) + 1
    return result

def get_total(emo_count):
    total = 0
    for emo, count in emo_count.items():
        total += count
    return total

def creat_file(total_count, emo_count, out_file):
    with open(out_file, 'w+') as result_f:
        result_f.write('Total count of emotion.\n' + str(total_count) + '\n\n')

        result_f.write('Number for each emotion.' + '\n')
        for key, value in sorted(emo_count.items(), key=lambda x: x[1], reverse=True):
            result_f.write('{0:<12}'.format(key) + ':\t' + '{0:>3}'.format(str(value)) + '\n')

def system_emo_count():
    in_file, out_file = get_files()
    emo_count = {}
    with open(in_file, 'r') as in_f:
        for line in in_f:
            emos = line.rstrip().split('\t')[2:]
            emo_count = get_emo_count(emos, emo_count)
    total_count = get_total(emo_count)
    creat_file(total_count, emo_count, out_file)

if __name__ == '__main__':
    system_emo_count()
