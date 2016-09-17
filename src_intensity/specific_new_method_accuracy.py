# -*- coding: utf-8 -*-
import sys


def get_files():
    intensity = sys.argv[1]
    base_path = '/home/sadayuki/Dropbox/Data-Mining-Research/'
    manual_file = base_path + 'data_intensity/sep_intensity/manual_classification/' + intensity
    new_method_file = base_path + 'data_intensity/sep_intensity/new_method/' + intensity
    out_file = base_path + 'data_intensity/accuracy/' + intensity
    return manual_file, new_method_file, out_file

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
            emo_scores = line[2].split(' ')
            emos = []
            for emo_score in emo_scores:
                emo = emo_score.split(':')[0]
                emos.append(emo)
            if file_name == 'new_method':
                emos = rm_score(emos)
            emo_list.append([id, emos])
    return sorted(emo_list, key=lambda x: x[0])

def is_id_ok(human_emo_list, after_news_emo_list):
    is_ok = True
    for human_id, system_id in zip(human_emo_list, after_news_emo_list):
        if human_id[0] != system_id[0]:
            is_ok = False
    if is_ok:
        print('ID no problem.')
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

def precision_input_total(system_emo_list):
    total = {}
    for each in system_emo_list:
        emos = each[1]
        for emo in emos:
            total[emo] = total.get(emo, 0) + 1
    result = {}
    for emo, total in total.items():
        result[emo] = {'total': total, 'match': 0, 'precision': 0}
    return result

def get_precision_each_emo(human_emo_list, system_emo_list):
    # will be look like, {'joy':{'total':a, 'match':b}, 'trust':...}
    emo_dict = precision_input_total(system_emo_list)

    for human, system in zip(human_emo_list, system_emo_list):
        human_emos, system_emos = human[1], system[1]
        for system_emo in system_emos:
            if system_emo in human_emos:
                emo_dict[system_emo]['match'] += 1

    result = emo_dict
    for emo, stat in emo_dict.items():
        emo_name = result[emo]
        emo_name['precision'] = emo_name['match'] / emo_name['total'] * 100

    return result

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

def recall_input_total(human_emo_list):
    total = {}
    for each in human_emo_list:
        emos = each[1]
        for emo in emos:
            total[emo] = total.get(emo, 0) + 1
    result = {}
    for emo, total in total.items():
        result[emo] = {'total': total, 'match': 0, 'recall': 0}
    return result

def get_recall_each_emo(human_emo_list, system_emo_list):
    # will be look like, {'joy':{'total':a, 'match':b}, 'trust':...}
    emo_dict = recall_input_total(human_emo_list)

    for human, system in zip(human_emo_list, system_emo_list):
        human_emos, system_emos = human[1], system[1]
        for human_emo in human_emos:
            if human_emo in system_emos:
                emo_dict[human_emo]['match'] += 1

    result = emo_dict
    for emo, stat in emo_dict.items():
        emo_name = result[emo]
        emo_name['recall'] = emo_name['match'] / emo_name['total'] * 100

    return result

def creat_file(precision_easy, precision, precision_each_emo, recall, recall_each_emo, out_file):
    with open(out_file, 'w+') as f:
        f.write('Precision Easy ' + str(precision_easy) + '\n\n')
        f.write('Precision ' + str(precision) + '\n\n')
        f.write('Precision for each emotion\n')
        for emo, stat_dict in precision_each_emo.items():
            f.write(emo + ' ' + str(stat_dict['precision']) + '\n')
        f.write('\n')

        f.write('Recall ' + str(recall) + '\n\n')
        f.write('Recall for each emotion\n')
        for emo, stat_dict in recall_each_emo.items():
            f.write(emo + ' ' + str(stat_dict['recall']) + '\n')

def get_accuracy():
    manual_file, new_method_file, out_file = get_files()

    # Get sorted list like belhuman_emo_listow.
    # [[ID,[emo, emo, ...]], [ID,[emo, emo, ...]], ...]
    human_emo_list = get_emo_list(manual_file, file_name='human')
    new_method_emo_list = get_emo_list(new_method_file, file_name='new_method')

    is_id_ok(human_emo_list, new_method_emo_list)

    precision_easy = get_precision_easy(human_emo_list, new_method_emo_list)
    print('Precision Easy:', precision_easy)

    precision = get_precision(human_emo_list, new_method_emo_list)
    print('Precision:', precision)

    precision_each_emo = get_precision_each_emo(human_emo_list, new_method_emo_list)
    print('Precision each emo:', precision_each_emo)

    recall = get_recall(human_emo_list, new_method_emo_list)
    print('recall:', recall)

    recall_each_emo = get_recall_each_emo(human_emo_list, new_method_emo_list)
    print('Recall each emo:', recall_each_emo)

    creat_file(precision_easy, precision, precision_each_emo, recall, recall_each_emo, out_file)

# ATTENTION: argv[1] for intensity, both, only_strong, only_weak
if __name__ == '__main__':
    get_accuracy()
