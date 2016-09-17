def get_files():
    base_path = '/home/sadayuki/Dropbox/Data-Mining-Research/'
    in_file = base_path + 'data_combined_results/original/human_sentiment'
    out_file  = base_path + 'data_combined_results/ids_to_be_rm/none'
    return in_file, out_file

def create_none():
    in_file, out_file = get_files()
    id_list = []
    with open(in_file, 'r') as in_f, open(out_file, 'w+') as out_f:
        for line in in_f:
            line = line.rstrip().split('\t')
            id, emo = line[0], line[-1]
            if emo == 'none':
                id_list.append(id)

        id_list = sorted(id_list)
        for id in id_list:
            out_f.write(id + '\n')

if __name__ == '__main__':
    create_none()
