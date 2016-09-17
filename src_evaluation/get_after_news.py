# -*- coding: utf-8 -*-
import sys


def get_files(MEAN_RATE, NEWS_RATE):
    base_path = '/home/sadayuki/Dropbox/Data-Mining-Research/'\
                'data_combined_results/new_approach_final/'
    in_file = base_path + 'after_mean/' + MEAN_RATE
    out_file  = base_path + 'after_news/mean' + MEAN_RATE + '/' + NEWS_RATE
    return in_file, out_file

def multiply_rate(emotions, NEWS_RATE):
    NEWS_RATE = float(NEWS_RATE.replace('_', '.'))
    result = []
    for emotion in emotions:
        name_score = emotion.split(':')
        name, score = name_score[0], float(name_score[1])
        if name == 'news':
            score *= NEWS_RATE
        result.append([name, score])
    return sorted(result, key=lambda x: x[1])

def rm_bigger_than_news(emotions, NEWS_RATE):
    result = []
    emotions = multiply_rate(emotions, NEWS_RATE)
    for emotion in emotions:
        emo_name = emotion[0]
        if emo_name == 'news':
            if result == []:
                result.append(['none', 0.0])
            break
        result.append(emotion)
    return result

def make_emo_str(emo):
    return emo[0] + ':' + str(emo[1])

def create_output_file(after_news, out_f):
    for each in after_news:
        id, text, emos = each[0], each[1], each[2]
        out_f.write(id + '\t' + text + '\t')
        for emo in emos:
            emo_str = make_emo_str(emo)
            out_f.write(emo_str + ' ')
        out_f.write('\n')

def get_after_mean(MEAN_RATE, NEWS_RATE):
    in_file, out_file = get_files(MEAN_RATE, NEWS_RATE)
    after_news = []

    with open(in_file, 'r') as in_f:
        for line in in_f:
            line = line.strip().split('\t')
            id, text, emotions = line[0], line[1], line[2].split(' ')
            emotions = rm_bigger_than_news(emotions, NEWS_RATE)
            after_news.append([id, text, emotions])

    with open(out_file, 'w+') as out_f:
        create_output_file(after_news, out_f)

if __name__ == '__main__':
    for mean in range(1, 71):
        MEAN_RATE = str(float(mean) / 10).replace('.', '_')
        for news in range(80, 101):
            NEWS_RATE = str(float(news) / 100).replace('.', '_')
            get_after_mean(MEAN_RATE, NEWS_RATE)
