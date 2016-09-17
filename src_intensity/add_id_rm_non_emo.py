# -*- coding: utf-8 -*-
import glob


def write_file(result_f, id_f, out_f):
    for result_line, id_line in zip(result_f, id_f):
        id = id_line.rstrip().split('\t')[-1]
        result_line = id + '\t' + result_line
        out_f.write(result_line)

def get_files():
    base_path = '/home/sadayuki/Dropbox/Data-Mining-Research/'
    result_files = glob.glob(base_path + 'data_evaluation/human_results/stat_results/*')
    id_files = glob.glob(base_path + 'data_testing/manual_classification/8_shuffled/*')
    out_file  = base_path + 'data_emotion_strength/id_added/stat_with_id'
    return result_files, id_files, out_file

def get_id_file(result_file, id_files):
    result = ''
    for id_file in id_files:
        if id_file.split('/')[-1] == result_file.split('/')[-1]:
            return id_file

def combine_in_files():
    result_files, id_files, out_file = get_files()
    with open(out_file, 'w+') as out_f:
        for result_file in result_files:
            id_file = get_id_file(result_file, id_files)
            with open(result_file, 'r') as result_f, open(id_file, 'r') as id_f:
                write_file(result_f, id_f, out_f)

if __name__ == '__main__':
    combine_in_files()
