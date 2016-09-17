# -*- coding: utf-8 -*-
import sys

def create_news_ave_dict(news_file):
    news_ave_dict = {}
    with open(news_file, 'r') as news_f:
        for line in news_f:
            line = line.strip().split(' ')
            emo, score = line[0], line[1]
            news_ave_dict[emo] = score
    return news_ave_dict

def create_emo_dict(emotions):
    emo_dict = {}
    for pair in emotions:
        pair = pair.split(':')
        emo_dict[pair[0]] = pair[1]
    return emo_dict

def reduce_emo_dict(emo_dict, token_num, news_ave_dict):
    reduced_emo_dict = {}
    for emo, score in emo_dict.items():
        normalized_score = float(score) / token_num
        if normalized_score < float(news_ave_dict[emo]):
            reduced_emo_dict[emo] = normalized_score
    return reduced_emo_dict

def reduce_emo(emotion_file, news_ave_dict):
    reduced_emo = {}
    with open(emotion_file, 'r') as emo_f:
        for line in emo_f:
            line = line.strip().split('\t')
            text, emotions = line[0], line[1:]
            emo_dict = create_emo_dict(emotions)
            token_num = len(text.split(' '))
            emo_dict = reduce_emo_dict(emo_dict, token_num, news_ave_dict)
            reduced_emo[text] = emo_dict
    return reduced_emo

def make_output_file(reduced_emo, out_file):
    with open(out_file, 'w+') as out_f:
        for text, emo_dict in reduced_emo.items():
            out_f.write(text + '\n')
            for emo, score in emo_dict.items():
                out_f.write(emo + ' ' + str(score) + '\n')
            out_f.write('\n')

def cut_more_than_news(emotion_file, news_file, out_file):
    news_ave_dict = create_news_ave_dict(news_file)
    reduced_emo  = reduce_emo(emotion_file, news_ave_dict)
    make_output_file(reduced_emo, out_file)

if __name__ == '__main__':
    MIN_FREQ  = sys.argv[1]
    EMOTION   = sys.argv[2]
    base_path = '/home/sadayuki/Dropbox/Data-Mining-Research/'
    emotion_file = base_path + 'data_system/testing/tokenized/minFreq_' + MIN_FREQ + '_score/' + EMOTION
    news_file = base_path + 'data_evaluation/news_score_ave/minFreq_' + MIN_FREQ
    out_file  = base_path + 'data_evaluation/cut_more_than_news/minFreq_' + MIN_FREQ + '/' + EMOTION

    cut_more_than_news(emotion_file, news_file, out_file)
