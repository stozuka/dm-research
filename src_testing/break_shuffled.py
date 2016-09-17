def make_sep_list():
    sep_list = []
    for i in range(20):
        sep_list.append(19 + 20 * i)
    return sep_list

def get_file_num(i):
    sep_list = make_sep_list()
    for idx, sep in enumerate(sep_list):
        if i <= sep:
            return idx + 1

def get_files():
    base_path = '/home/sadayuki/Dropbox/Data-Mining-Research/'
    in_file = base_path + 'data_testing/manual_classification/shuffled_combined_testing_data.txt'
    out_dir  = base_path + 'data_testing/manual_classification/8_shuffled/'
    return in_file, out_dir

def break_file():
    in_file, out_dir = get_files()
    with open(in_file, 'r') as in_f:
        for i, line in enumerate(in_f):
            file_num = str(get_file_num(i))
            with open(out_dir + 'result_' + file_num, 'a+') as out_f:
                out_f.write(line)

if __name__ == '__main__':
    break_file()