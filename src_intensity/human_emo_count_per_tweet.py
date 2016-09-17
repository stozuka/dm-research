# -*- coding: utf-8 -*-
import sys
import glob


def get_files():
    base_path = '/home/sadayuki/Dropbox/Data-Mining-Research/data_intensity/'
    in_files = glob.glob(base_path + 'sep_intensity/manual_classification/*')
    out_dir  = base_path + 'emo_count_per_tweet/manual_classification/'
    return in_files, out_dir

def get_emo_count(emos, emo_count):
    result = emo_count
    for emo in emos:
        emo = emo.split(':')[0]
        result[emo] = result.get(emo, 0) + 1
    return result

def get_total(emo_count):
    total = 0
    for emo, count in emo_count.items():
        total += count
    return total

def get_num_per_tweet(emos, num_per_tweet):
    result = num_per_tweet
    num = str(len(emos))
    result[num] = result.get(num, 0) + 1
    return result

def creat_file(total_count, num_per_tweet, emo_count, out_file):
    with open(out_file, 'w+') as result_f:
        result_f.write('Total count of emotion.\n' + str(total_count) + '\n\n')

        result_f.write('Number of emotions per tweet.' + '\n')
        tweet_count = 0
        for key, value in sorted(num_per_tweet.items(), key=lambda x: int(x[0])):
            result_f.write(key + ' emotion(s): ' + '{0:>3}'.format(str(value)) + '\n')
            tweet_count += value
        result_f.write('total count of tweet ' + str(tweet_count) + '\n')
        result_f.write('\n')

        result_f.write('Number for each emotion.' + '\n')
        for key, value in sorted(emo_count.items(), key=lambda x: x[1], reverse=True):
            result_f.write('{0:<12}'.format(key) + ':\t' + '{0:>3}'.format(str(value)) + '\n')

def get_emos(line):
    emos = line.split('\t')[-1].split()
    result = [emo.split(':')[0] for emo in emos]
    return result

def human_emo_count():
    in_files, out_dir = get_files()
    emo_count = {}
    for in_file in in_files:
        num_per_tweet= {}
        emo_count = {}
        intensity = in_file.split('/')[-1]
        print('Processing', intensity)
        with open(in_file, 'r') as in_f:
            for line in in_f:
                line = line.strip()
                emos = get_emos(line)
                num_per_tweet = get_num_per_tweet(emos, num_per_tweet)
                emo_count = get_emo_count(emos, emo_count)
        total_count = get_total(emo_count)
        out_file = out_dir + in_file.split('/')[-1]
        creat_file(total_count, num_per_tweet, emo_count, out_file)

if __name__ == '__main__':
    human_emo_count()
