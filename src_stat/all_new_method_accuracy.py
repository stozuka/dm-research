# -*- coding: utf-8 -*-
import sys


def get_files(mean1, mean2):
    # std = str(600)
    when = sys.argv[1]
    std = sys.argv[2]

    base_path = '/home/sadayuki/Dropbox/Data-Mining-Research/'

    human_emo_file = base_path + 'data_combined_results/rm_none/human_sentiment'

    after_mean_2_emo_file = base_path + 'data_combined_results/new_approach_final/after_mean_2_' + when + '/std_' + std + '/mean1_' + mean1 + '/mean2_' + mean2

    out_file = base_path + 'data_stat_final/best_accuracy/without_news/news0_93_std' + std + '_' + when

    return human_emo_file, after_mean_2_emo_file, out_file

def rm_score(emos):
    result = []
    for emo in emos:
        emo = emo.split(':')[0]
        result.append(emo)
    return result

def get_emo_list(emo_file, file_name=''):
    emo_list = []
    with open(emo_file, 'r') as f:
        for line in f:
            line = line.strip().split('\t')
            id= line[0]
            emos = line[2].split(' ')
            if file_name == 'after_news':
                emos = rm_score(emos)
            emo_list.append([id, emos])
    return sorted(emo_list, key=lambda x: x[0])

def is_id_ok(human_emo_list, after_news_emo_list):
    is_ok = True
    for human_id, system_id in zip(human_emo_list, after_news_emo_list):
        if human_id[0] != system_id[0]:
            is_ok = False
    if is_ok:
        # print('ID no problem.')
        pass
    else:
        print("ID doesn't match.")

def get_precision_easy(human_emo_list, after_news_emo_list):
    included = 0

    for human, system in zip(human_emo_list, after_news_emo_list):
        human_emos, system_emos = human[1], system[1]
        for system_emo in system_emos:
            if system_emo in human_emos:
                included += 1
                break

    precision_easy = included / len(after_news_emo_list) * 100
    return precision_easy

def get_precision(human_emo_list, after_news_emo_list):
    included = 0
    not_included = 0

    for human, system in zip(human_emo_list, after_news_emo_list):
        human_emos, system_emos = human[1], system[1]
        for system_emo in system_emos:
            if system_emo in human_emos:
                included += 1
            else:
                not_included += 1

    precision = included / (included + not_included) * 100
    return precision

def get_recall(human_emo_list, after_news_emo_list):
    included = 0
    not_included = 0

    for human, system in zip(human_emo_list, after_news_emo_list):
        human_id, system_id = human[0], system[0]
        human_emos, system_emos = human[1], system[1]
        for human_emo in human_emos:
            if human_emo in system_emos:
                included += 1
            else:
                not_included += 1

    recall = included / (included + not_included) * 100
    return recall

def creat_file(precision_easy, precision, recall, out_file, mean1, mean2):
    with open(out_file, 'a+') as f:
        f.write(mean1 + ' ' + mean2 + '\n')
        f.write('precision_easy ' + str(precision_easy) + '\n')
        f.write('precision ' + str(precision) + '\n')
        f.write('recall ' + str(recall) + '\n')
        total = precision_easy + precision + recall
        f.write('total ' + str(total) + '\n')

def get_accuracy(mean1, mean2):
    human_emo_file, after_mean_2_emo_file, out_file = get_files(mean1, mean2)

    # Get sorted list like belhuman_emo_listow.
    # [[ID,[emo, emo, ...]], [ID,[emo, emo, ...]], ...]
    human_emo_list = get_emo_list(human_emo_file, file_name='human')
    after_mean_2_emo_list = get_emo_list(after_mean_2_emo_file, file_name='after_news')

    is_id_ok(human_emo_list, after_mean_2_emo_list)

    precision_easy = get_precision_easy(human_emo_list, after_mean_2_emo_list)
    # print('Precision Easy:', precision_easy)
    precision = get_precision(human_emo_list, after_mean_2_emo_list)
    # print('Precision:', precision)
    recall = get_recall(human_emo_list, after_mean_2_emo_list)
    # print('recall:', recall)

    if precision >= 49.24 and recall >= 47.90:
        print('mean1:', mean1, 'mean2:', mean2)
        print('precision_easy:', precision_easy)
        print('precision:', precision, 'recall:', recall)
        print('total:', precision + recall)
        print()
        creat_file(precision_easy, precision, recall, out_file, mean1, mean2)

# ATTENTION: argv[1] for std, argv[2] for time threshold
if __name__ == '__main__':
    for mean1 in range(1, 71):
        mean1 = str(float(mean1) / 10).replace('.', '_')
        for mean2 in range(1, 71):
            mean2 = str(float(mean2) / 10).replace('.', '_')
            print('Processing', mean1, mean2)
            get_accuracy(mean1, mean2)
