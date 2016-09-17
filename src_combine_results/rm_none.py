import glob
import os

def get_files():
    base_path = '/home/sadayuki/Dropbox/Data-Mining-Research/'
    in_files = glob.glob(base_path + 'data_combined_results/original/*')
    out_path  = base_path + 'data_combined_results/rm_none/'
    id_file = base_path + 'data_combined_results/ids_to_be_rm/none'
    return in_files, out_path, id_file

def get_id_list(id_file):
    id_list = []
    with open(id_file, 'r') as id_f:
        for line in id_f:
            id_list.append(line.rstrip())
    return id_list

def create_out_files():
    in_files, out_path, id_file = get_files()
    for in_file in in_files:
        if os.path.isdir(in_file):
            continue
        file_name = in_file.split('/')[-1]
        out_file = out_path + file_name
        id_list = get_id_list(id_file)
        with open(in_file, 'r') as in_f, open(out_file, 'w+') as out_f:
            for line in in_f:
                id = line.split('\t')[0]
                if not id in id_list:
                    out_f.write(line)

if __name__ == '__main__':
    create_out_files()
