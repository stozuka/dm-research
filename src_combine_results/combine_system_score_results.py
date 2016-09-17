# -*- coding: utf-8 -*-
import glob


def get_id_list(in_file):
    id_list = []
    emotion = in_file.split('/')[-1].split('_')[0]
    id_file = '/home/sadayuki/Dropbox/Data-Mining-Research/data_testing/final_50/final_50_' + emotion
    with open(id_file, 'r') as id_f:
        for line in id_f:
            id = line.strip().split('\t')[-1]
            id_list.append(id)
    return id_list

def write_file(in_file, out_f):
    id_list = get_id_list(in_file)
    counter = 0
    with open(in_file, 'r') as in_f:
        for idx, line in enumerate(in_f):
            if not line == '\n':
                out_f.write(id_list[counter] + '\t' + line.strip() + '\n')
                counter += 1

def get_files():
    base_path = '/home/sadayuki/Dropbox/Data-Mining-Research/'
    in_files = glob.glob(base_path + 'data_system/testing/tokenized/minFreq_15_score/*')
    out_file  = base_path + 'data_combined_results/original/system_score_final'
    return in_files, out_file

def combined_in_files():
    in_files, out_file = get_files()
    with open(out_file, 'w+') as out_f:
        for in_file in in_files:
            write_file(in_file, out_f)

if __name__ == '__main__':
    combined_in_files()
