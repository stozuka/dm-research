# -*- coding: utf-8 -*-
import sys
import glob


def get_files(MEAN_RATE):
    base_path = '/home/sadayuki/Dropbox/Data-Mining-Research/'
    in_files = glob.glob(base_path + 'data_combined_results/new_approach_final/after_news/mean' + MEAN_RATE + '/*')
    out_file  = base_path + 'data_stat_final/after_news_emo_count/' + MEAN_RATE
    return in_files, out_file

def count_emo(in_f):
    sum = 0
    for line in in_f:
        emos = line.strip().split('\t')[-1].split(' ')
        sum += len(emos)
    return sum

def create_out_file(count_list, after_mean_emo_count, out_f):
    for rate, count in sorted(count_list, key=lambda x: x[0]):
        out_f.write('News rate: ' + '{0:>4}'.format(str(rate)) + '\n')
        out_f.write('Total: ' + '{0:>4}'.format(str(count)) + '\n')
        out_f.write('Removed: ' + str(after_mean_emo_count - count) + '\n')
        out_f.write('(After mean: ' + str(after_mean_emo_count) + ')\n\n')

def count_emo_after_news(MEAN_RATE, after_mean_emo_count):
    in_files, out_file = get_files(MEAN_RATE)
    count_list = []

    for in_file in in_files:
        with open(in_file, 'r') as in_f:
            rate = float(in_file.split('/')[-1].replace('_', '.'))
            number = count_emo(in_f)
            count_list.append([rate, number])

    with open(out_file, 'w+') as out_f:
        create_out_file(count_list, after_mean_emo_count, out_f)

def get_after_mean_count(mean):
    count_file = '/home/sadayuki/Dropbox/Data-Mining-Research/'\
                 'data_stat/after_mean_emo_count'
    with open(count_file, 'r') as f:
        for line in f:
            line_list = line.strip().split()
            if mean == float(line_list[0]):
                return int(line_list[1])

if __name__ == '__main__':
    for mean in range(1, 71):
        after_mean_emo_count = get_after_mean_count(float(mean) / 10)
        MEAN_RATE = str(float(mean) / 10).replace('.', '_')
        print('Processing', MEAN_RATE)
        count_emo_after_news(MEAN_RATE, after_mean_emo_count)
