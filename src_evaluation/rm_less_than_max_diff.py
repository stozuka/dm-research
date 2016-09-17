# -*- coding: utf-8 -*-
import sys

def remove_text_from_line(in_file):
    result = []
    with open(in_file, 'r') as i_f:
        for line in i_f:
            result.append(line.strip().split('\t')[1:])
    return result

def get_array_of_scores(scores):
    result = []
    for tweet in scores:
        each_tweet = []
        for score in tweet:
            temp = score.split(':')
            each_tweet.append([temp[0], float(temp[1])])
        result.append(each_tweet)
    return result

def get_sorted(scores_array):
    result = []
    for item in scores_array:
        sorted_result = sorted(item, key=lambda x:x[1])
        result.append(sorted_result)
    return result

def get_score_diff_array(emo_score):
    score_diff = []
    for idx, item in enumerate(emo_score):
        if idx == len(emo_score) - 1:
            break
        score_diff.append(emo_score[idx + 1] - emo_score[idx])
    return score_diff

def get_idx_of_max_diff(tweet):
    emo_score = []
    for item in tweet:
        emo_score.append(item[1])
    score_diff = get_score_diff_array(emo_score)
    return score_diff.index(max(score_diff))

def output(out_file, sorted_scores):
    with open(out_file, 'w+') as o_f:
        for item in sorted_scores:
            max_idx = get_idx_of_max_diff(item)
            for idx, emotion in enumerate(item):
                if idx < max_idx + 1:
                    o_f.write(item[idx][0] + ' ' + str(item[idx][1]) + '\t')
            o_f.write('\n')

def create_out_file(in_file, out_file):
    scores        = remove_text_from_line(in_file)
    scores_array  = get_array_of_scores(scores)
    sorted_scores = get_sorted(scores_array)
    output(out_file, sorted_scores)

if __name__ == '__main__':
    EMOTION   = sys.argv[1]
    # min_freq  = sys.argv[2]
    base_path = '/home/sadayuki/Dropbox/Data-Mining-Research/'
    # in_file   = base_path + 'data_system/testing/tokenized/minFreq_' + min_freq + '_score/' + EMOTION
    in_file   = base_path + 'data_system/testing/tokenized/news_purified_score/' + EMOTION + '_score'
    out_file  = base_path + 'data_evaluation/biggest_diff/news_purified/' + EMOTION

    create_out_file(in_file, out_file)
