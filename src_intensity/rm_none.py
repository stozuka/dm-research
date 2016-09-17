import glob
import os

def get_files():
    base_path = '/home/sadayuki/Dropbox/Data-Mining-Research/'
    in_file = base_path + 'data_intensity/id_added/stat_with_id'
    out_file  = base_path + 'data_intensity/rm_none/rm_none'
    id_file = base_path + 'data_combined_results/ids_to_be_rm/none'
    return in_file, out_file, id_file

def get_id_list(id_file):
    id_list = []
    with open(id_file, 'r') as id_f:
        for line in id_f:
            id_list.append(line.rstrip())
    return id_list

def create_out_files():
    in_file, out_file, id_file = get_files()

    id_list = get_id_list(id_file)
    with open(in_file, 'r') as in_f, open(out_file, 'w+') as out_f:
        for line in in_f:
            id = line.split('\t')[0]
            if not id in id_list:
                out_f.write(line)

if __name__ == '__main__':
    create_out_files()
