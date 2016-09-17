# -*- coding: utf-8 -*-
import sys
import numpy as np


def get_files(mean1, mean2):
    base_path = '/home/sadayuki/Dropbox/Data-Mining-Research/'\
                'data_combined_results/new_approach/'
    # 1_0(1.0) is the weight for news.
    in_file   = base_path + 'after_mean_2/mean1_' + mean1 + '/mean2_' + mean2
    out_file  = base_path + 'after_biggest_diff/mean1_' + mean1 + '/mean2_' + mean2
    return in_file, out_file

def break_into_list(emos):
    result = []
    for emo in emos:
        emo_list = emo.split(':')
        emo_name, emo_score = emo_list[0], emo_list[1]
        result.append([emo_name, float(emo_score)])
    return sorted(result, key=lambda x: x[1])

def get_max_diff_idx(emo_score_list):
    max_diff = 0
    max_diff_idx = 0

    for idx in range(len(emo_score_list) - 1):
        diff = float(emo_score_list[idx][1]) - float(emo_score_list[idx + 1][1])
        if diff > max_diff:
            max_diff = diff
            max_diff_idx = idx

    return max_diff_idx

def remove_emotions(emo_score_list, mean2):
    result = []
    max_diff_idx = get_max_diff_idx(emo_score_list)
    result = emo_score_list[:max_diff_idx + 1]
    return result

def extract_scores(emo_score_list):
    result = []
    for each in emo_score_list:
        result.append(each[1])
    return result

def get_standard_deviation(emo_score_list):
    scores = extract_scores(emo_score_list)
    data = np.array(scores)
    std = np.std(data)
    return std

def process_emos(emos, mean2, token_num):
    STD_THRE = float(sys.argv[1])
    emo_score_list = break_into_list(emos)

    # If having only one emotion or std is below threshold,
    # no process is needed
    # Normalize using token_num
    std = get_standard_deviation(emo_score_list) / token_num
    if len(emo_score_list) <= 2 or std < STD_THRE:
        return emo_score_list
    # Otherwise, process below is needed
    else:
        return remove_emotions(emo_score_list, mean2)

def calculation(in_f, mean2):
    result = []
    for line in in_f:
        line = line.strip().split('\t')
        id_text, emos = line[:2], line[2].split(' ')
        token_num = len(id_text[1].split())
        emos_list = process_emos(emos, mean2, token_num)
        id_text.append(emos_list)
        result.append(id_text)
    return result

def create_out_file(after_mean_2, out_f):
    for each in after_mean_2:
        out_f.write(each[0] + '\t' + each[1] + '\t')
        for emo in each[2]:
            out_f.write(emo[0] + ':' + str(emo[1]) + ' ')
        out_f.write('\n')

def get_after_biggest_diff(mean1, mean2):
    in_file, out_file = get_files(mean1, mean2)
    after_mean_2 = []

    with open(in_file, 'r') as in_f:
        after_mean_2 = calculation(in_f, mean2)

    with open(out_file, 'w+') as out_f:
        create_out_file(after_mean_2, out_f)

# ATTENTION:
# argv[1] for std threshold
if __name__ == '__main__':
    for mean1 in range(1, 31):
        mean1 = str(float(mean1) / 10).replace('.', '_')
        for mean2 in range(1, 31):
            mean2 = str(float(mean2) / 10).replace('.', '_')
            print('Processing', mean1, mean2)
            get_after_biggest_diff(mean1, mean2)
