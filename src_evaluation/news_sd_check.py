# -*- coding: utf-8 -*-
import sys
import numpy as np

def split_line(line):
    result = {}
    temp = line.strip().split('\t')
    text = temp[0]
    all_emo_score = {}
    for each_emo in temp[1:]:
        emo_score = each_emo.split(':')
        all_emo_score[emo_score[0]] = float(emo_score[1])
        result[text] = all_emo_score
    return result

def get_all_tweets_array(in_file):
    all_tweets = []
    with open(in_file, 'r') as in_f:
        for line in in_f:
            all_tweets.append(split_line(line))
    return all_tweets

def remove_zero(all_tweets):
    zero_removed = []
    for each_item in all_tweets:
        is_zero = False
        for text, emo_score in each_item.items():
            for emo, score in emo_score.items():
                if score == 0.0:
                    is_zero = True
            if is_zero == False:
                zero_removed.append(each_item)
    return zero_removed

# TODO: Implement this function
def remove_low_score(all_tweets):
    high_sd_removed = []
    for each_item in all_tweets:
        is_zero = False
        score_list = []
        for text, emo_score in each_item.items():
            for emo, score in emo_score.items():
                score_list.append(score)
            score_data = np.array(score_list)
            mean = np.mean(score_data)
            unit_score = mean / len(text.split(' '))
            if unit_score > 3500:
                high_sd_removed.append(each_item)

    return high_sd_removed

def devide_score(all_tweets):
    new_all_tweets = []
    for tweet in all_tweets:
        new_tweet = {}
        for text, emo_score in tweet.items():
            token_size = len(text.split(' '))
            new_emo_score = {}
            for emo, score in emo_score.items():
                score /= token_size
                new_emo_score[emo] = score
            new_tweet[text] = new_emo_score
        new_all_tweets.append(new_tweet)
    return new_all_tweets

def get_sum_dict(all_tweets):
    array_size = len(all_tweets)
    sum_dict = {}
    for tweet in all_tweets:
        for text, emo_score in tweet.items():
            for emo, score in emo_score.items():
                sum_dict[emo] = sum_dict.get(emo, 0) + score
    sum_dict_devided = {}
    for emo, score in sum_dict.items():
        sum_dict_devided[emo] = score / array_size
    return sum_dict_devided

def make_output_file(sum_dict, out_file):
    with open(out_file, mode='w+') as out_f:
        for emo, score in sum_dict.items():
            out_f.write(emo + ' ' + str(score) + '\n')

def get_news_ave(in_file, out_file):
    all_tweets = get_all_tweets_array(in_file)
    all_tweets = remove_zero(all_tweets)

    all_tweets = remove_low_score(all_tweets)

    all_tweets = devide_score(all_tweets)
    sum_dict = get_sum_dict(all_tweets)
    for emo, score in sum_dict.items():
        print(emo, score)
    make_output_file(sum_dict, out_file)

if __name__ == '__main__':
    MIN_FREQ  = sys.argv[1]
    base_path = '/home/sadayuki/Dropbox/Data-Mining-Research/'
    in_file   = base_path + 'data_system/testing/tokenized/minFreq_' + MIN_FREQ + '_score/news_10000'
    out_file  = base_path + 'data_evaluation/news_score_ave/minFreq_' + MIN_FREQ

    get_news_ave(in_file, out_file)
