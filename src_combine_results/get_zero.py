def get_files():
    base_path = '/home/sadayuki/Dropbox/Data-Mining-Research/'
    in_file = base_path + 'data_combined_results/original/system_score'
    out_file  = base_path + 'data_combined_results/ids_to_be_rm/zero'
    return in_file, out_file

def create_zero():
    in_file, out_file = get_files()
    with open(in_file, 'r') as in_f, open(out_file, 'w+') as out_f:
        for line in in_f:
            line = line.rstrip().split('\t')
            id, emos_str = line[0], ' '.join(line[2:])
            if ':0.0' in emos_str:
                out_f.write(id + '\n')

if __name__ == '__main__':
    create_zero()
