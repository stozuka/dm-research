def get_files():
    base_path = '/home/sadayuki/Dropbox/Data-Mining-Research/'\
                'data_combined_results/ids_to_be_rm/'
    none_file = base_path + 'none'
    zero_file  = base_path + 'zero'
    all_file = base_path + 'all'
    return none_file, zero_file, all_file

def append_id(file_name, id_list=[]):
    result = id_list
    with open(file_name, 'r') as f:
        for line in f:
            line = int(line.rstrip())
            result.append(line)
    return result

def create_file(id_list, all_file):
    id_list = sorted(list(set(id_list)))
    with open(all_file, 'w+') as all_f:
        for id in id_list:
            all_f.write(str(id) + '\n')

def get_all():
    none_file, zero_file, all_file = get_files()
    id_list = append_id(none_file)
    id_list = append_id(zero_file, id_list)
    create_file(id_list, all_file)

if __name__ == '__main__':
    get_all()