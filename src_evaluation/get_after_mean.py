# -*- coding: utf-8 -*-
import sys


def get_files(rate):
    RATE = rate.replace('.', '_')
    base_path = '/home/sadayuki/Dropbox/Data-Mining-Research/'\
                'data_combined_results/'
    in_file   = base_path + 'rm_none/system_score_final'
    out_file  = base_path + 'new_approach_final/after_mean/' + RATE
    return in_file, out_file

def break_into_list(emos):
    result = []
    for emo in emos:
        emo_list = emo.split(':')
        emo_name, emo_score = emo_list[0], emo_list[1]
        result.append([emo_name, float(emo_score)])
    return sorted(result, key=lambda x: x[1])

def rm_news(emo_score_list):
    no_news_list = []
    for emo_score in emo_score_list:
        if emo_score[0] != 'news':
            no_news_list.append(emo_score)
    return no_news_list

def get_mean(emo_score_list, rate):
    RATE = float(rate)
    sum = 0
    no_news_list = rm_news(emo_score_list)
    size = len(no_news_list)
    for idx in range(size - 1):
        sum += no_news_list[idx + 1][1] - no_news_list[idx][1]
    return sum / (size - 1) * RATE

def sep_news(emo_score_list):
    news = []
    no_news_list = []
    for emo_score in emo_score_list:
        if emo_score[0] == 'news':
            news = emo_score
        else:
            no_news_list.append(emo_score)
    return news, no_news_list

def process_emos(emos, rate):
    result = []
    emo_score_list = break_into_list(emos)
    mean = get_mean(emo_score_list, rate)
    news, no_news_list = sep_news(emo_score_list)
    for idx in range(len(no_news_list) - 1):
        result.append(no_news_list[idx])
        if no_news_list[idx + 1][1] - no_news_list[idx][1] > mean:
            break
    result.append(news)
    return sorted(result, key=lambda x: x[1])

def calculation(in_f, rate):
    result = []
    for line in in_f:
        line = line.strip().split('\t')
        id_text, emos = line[:2], line[2:]
        emos_list = process_emos(emos, rate)
        id_text.append(emos_list)
        result.append(id_text)
    return result

def create_out_file(after_mean, out_f):
    for each in after_mean:
        out_f.write(each[0] + '\t' + each[1] + '\t')
        for emo in each[2]:
            out_f.write(emo[0] + ':' + str(emo[1]) + ' ')
        out_f.write('\n')

def get_after_mean(rate):
    in_file, out_file = get_files(rate)
    after_mean = []
    with open(in_file, 'r') as in_f:
        after_mean = calculation(in_f, rate)
    with open(out_file, 'w+') as out_f:
        create_out_file(after_mean, out_f)

# ATTENTION:
# Input float nuber into argv[1] which will be used in
# get_files and get_mean(emo_score_list):
if __name__ == '__main__':
    for rate in range(1, 71):
        rate = str(rate / 10)
        get_after_mean(rate)
