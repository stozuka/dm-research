# -*- coding: utf-8 -*-
import csv
import sys


def get_20_tweets(lines):
    result = []
    original_tweets = lines[0]
    for idx in range(0, 160, 8):
        result.append(' '.join(original_tweets[idx].split(' ')[:-1]))
    return result

def get_zipped_emo(lines):
    emo_line_1 = lines[1]
    emo_line_2 = lines[2]
    emo_line_3 = lines[3]
    result = []
    for first, second, third in zip(emo_line_1, emo_line_2, emo_line_3):
        result.append([first, second, third])
    return result

def get_emo_chunk_20(zipped_emo):
    result = []
    counter = 0
    chunk_20 = []
    for _ in range(0, 20):
        chunk_20.append(zipped_emo[counter : counter + 8])
        counter += 8

    for chunk in chunk_20:
        tweet_dict = {}
        for idx, scores in enumerate(chunk):
            if idx == 0:
                tweet_dict['joy'] = scores
            elif idx == 1:
                tweet_dict['trust'] = scores
            elif idx == 2:
                tweet_dict['fear'] = scores
            elif idx == 3:
                tweet_dict['surprise'] = scores
            elif idx == 4:
                tweet_dict['sadness'] = scores
            elif idx == 5:
                tweet_dict['disgust'] = scores
            elif idx == 6:
                tweet_dict['anger'] = scores
            elif idx == 7:
                tweet_dict['anticipation'] = scores
        result.append(tweet_dict)

    return result

def make_tweet_emo_list(tweets, emo_chunk_20):
    result = []
    for tweet, emo_chunk in zip(tweets, emo_chunk_20):
        result.append([tweet, emo_chunk])
    return result

def del_first_col(csv_reader):
    result = []
    for line in csv_reader:
        del line[0]
        result.append(line)
    return result

def get_emo_strength_dict():
    return {
        'なし':0,
        '弱':1,
        '中':2,
        '強':3
    }

def convert_str_to_int(list):
    result = [list[0]]
    for line in list[1:]:
        new_line = []
        for score in line:
            for strength, number in get_emo_strength_dict().items():
                if score == strength:
                    new_line.append(number)
        result.append(new_line)
    return result

def process_csv_reader(in_f):
    csv_reader = list(csv.reader(in_f, delimiter=',', quotechar='"'))
    csv_reader = del_first_col(csv_reader)
    csv_reader = convert_str_to_int(csv_reader)
    return csv_reader

def process_emo_chunk(result):
    zipped_emo = get_zipped_emo(result)
    emo_chunk_20 = get_emo_chunk_20(zipped_emo)
    return emo_chunk_20

def get_final_list(result):
    tweets = get_20_tweets(result)
    emo_chunk_20 = process_emo_chunk(result)
    final_list = make_tweet_emo_list(tweets, emo_chunk_20)
    return final_list

def create_stat_out_file(final_list, stat_out_f):
    for tw_emo_pair in final_list:
        stat_out_f.write(tw_emo_pair[0] + '\t')
        for emo, scores in tw_emo_pair[1].items():
            stat_out_f.write(emo + ' ')
            for score in scores:
                stat_out_f.write(str(score) + ' ')
            stat_out_f.write('\t')
        stat_out_f.write('\n')

def get_final_emotions(final_list):
    final_emotions = []
    for tw_emo_chunk in final_list:
        tweet = tw_emo_chunk[0]
        emotions = []
        for emo, scores in tw_emo_chunk[1].items():
            count = 0
            for score in scores:
                if score != 0:
                    count += 1
            if count >= 2:
                emotions.append(emo)
        final_emotions.append([tweet, emotions])
    return final_emotions

def create_emo_out_file(removed_zero_score_emo, emo_out_f):
    for tw_emo_pair in removed_zero_score_emo:
        emo_out_f.write(tw_emo_pair[0] + '\t')
        if not tw_emo_pair[1] == []:
            for emo in tw_emo_pair[1]:
                emo_out_f.write(emo + ' ')
        else:
            emo_out_f.write('none')
        emo_out_f.write('\n')

def process_result(in_file, stat_out_file, emo_out_file):
    with open(in_file, 'r') as in_f:
        result = process_csv_reader(in_f)
        final_list = get_final_list(result)

    with open(stat_out_file, 'w+') as stat_out_f:
        create_stat_out_file(final_list, stat_out_f)

    removed_zero_score_emo = get_final_emotions(final_list)

    with open(emo_out_file, 'w+') as emo_out_f:
        create_emo_out_file(removed_zero_score_emo, emo_out_f)

def get_files(result_number):
    base_path = '/home/sadayuki/Dropbox/Data-Mining-Research/data_evaluation/human_results/'
    in_file   = base_path + 'original_rm_dup/result_' + result_number + '.csv'
    stat_out_file  = base_path + 'stat_results/result_' + result_number
    emo_out_file = base_path + 'classification_results/result_' + result_number
    return in_file, stat_out_file, emo_out_file

if __name__ == '__main__':
    result_number  = sys.argv[1]
    in_file, stat_out_file, emo_out_file = get_files(result_number)
    process_result(in_file, stat_out_file, emo_out_file)
