# -*- coding: utf-8 -*-
import glob

def create_id_list(in_file):
    ids = []
    for line in in_file:
        id = line.split('\t')[1]
        ids.append(id)
    return ids

def file_io(in_file, out_file, in_file_name):
    with open(in_file, 'r') as in_file, open(out_file, 'w+') as out_file:
        counter = 0
        ids = create_id_list(in_file)
        for id in ids:
            out_file.write(id)
            counter += 1
        print(in_file_name + ' number of ids:' + str(counter))

def create_out_file(in_files, out_path):
    for in_file in in_files:
        in_file_name = in_file.split('/')[-1]
        out_file = out_path + in_file_name + '_ids'
        file_io(in_file, out_file, in_file_name)

if __name__ == '__main__':
    base_path = '/home/sadayuki/Dropbox/Data-Mining-Research/data_testing/'
    in_files = glob.glob(base_path + 'final_50/*')
    out_path  = base_path + 'final_50_ids/'

    create_out_file(in_files, out_path)
