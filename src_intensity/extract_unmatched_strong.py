# -*- coding: utf-8 -*-
import sys


def get_files():
    method = sys.argv[1]
    base_path = '/home/sadayuki/Dropbox/Data-Mining-Research/'
    manual_file = base_path + 'data_intensity/sep_' + method + '/manual_classification/strong'
    new_method_file = base_path + 'data_intensity/sep_' + method + '/new_method/strong'
    out_file = base_path + 'data_intensity/unmatched_strong/' + method
    return manual_file, new_method_file, out_file

def rm_score(emos):
    result = []
    for emo in emos:
        emo = emo.split(':')[0]
        result.append(emo)
    return result

def purify_emos(emos):
    result = []
    for emo in emos.split():
        emo, intensity = emo.split(':')
        result.append(emo)
    return result

def make_list(in_file, category=''):
    result = []
    with open(in_file, 'r') as f:
        for line in f:
            each_dict = {}
            id, text, emos = line.strip().split('\t')
            emos = purify_emos(emos)
            each_dict['id'] = int(id)
            each_dict['text'] = text
            each_dict[category] = emos
            result.append(each_dict)
    sorted(result, key=lambda x: x['id'])
    return result

def combine_list(human_list, system_list):
    combine_list = []
    for human in human_list:
        for system in system_list:
            if human['id'] == system['id']:
                human['system'] = system['system']
                combine_list.append(human)
    return combine_list

def make_unmatched(combine_list):
    unmateched_list = []
    for each in combine_list:
        human_emos = each['human']
        system_emos = each['system']
        is_matched = False
        for system_emo in system_emos:
            if system_emo in human_emos:
                is_matched = True
        if not is_matched:
            unmateched_list.append(each)
    return unmateched_list

def creat_file(unmateched_list, out_file):
    with open(out_file, 'w+') as f:
        for each in unmateched_list:
            f.write(str(each['id']) + '\t' + each['text'] + '\n')
            f.write('human emos:')
            for human_emo in each['human']:
                f.write(human_emo + ' ')
            f.write('\n')
            f.write('system emos:')
            for human_emo in each['system']:
                f.write(human_emo + ' ')
            f.write('\n\n')

def get_unmatched():
    human_file, system_file, out_file = get_files()
    human_list = make_list(human_file, category='human')
    system_list = make_list(system_file, category='system')
    combined_list = combine_list(human_list, system_list)
    unmateched_list = make_unmatched(combined_list)
    creat_file(unmateched_list, out_file)

    for idx, each in enumerate(unmateched_list):
        print(idx + 1, each)

# ATTENTION: argv[1] for intensity, both, only_strong, only_weak
if __name__ == '__main__':
    get_unmatched()
