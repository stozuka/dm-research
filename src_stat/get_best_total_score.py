# -*- coding: utf-8 -*-
import sys


def get_file():
    in_file = '/home/sadayuki/Dropbox/Data-Mining-Research/'\
           'data_stat/best_accuracy/news0_87_std800_fourth'
    # in_file = '/home/sadayuki/Dropbox/Data-Mining-Research/'\
    #        'data_stat/best_accuracy/normalized_std/news0_88'
    return in_file

def get_best_total_score():
    in_file = get_file()
    best_total = 0
    with open(in_file, 'r') as f:
        for line in f:
             line_list = line.strip().split()
             if line_list == []:
                 continue
             name = line_list[0]
             if name == 'total' and float(line_list[1]) >= best_total:
                 best_total = float(line_list[1])
    print(best_total)

if __name__ == '__main__':
    get_best_total_score()
