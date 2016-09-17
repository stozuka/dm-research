import glob


def get_files():
    base_path = '/home/sadayuki/Dropbox/Data-Mining-Research/'
    in_file = base_path + 'data_combined_results/new_approach/after_mean_2_first/std_600/mean1_1_8/mean2_1_7'
    sep_files = glob.glob(base_path + 'data_intensity/sep_majority/manual_classification/*')
    out_dir = base_path + 'data_intensity/sep_majority/new_method/'
    return in_file, sep_files, out_dir

def make_id_dict(sep_files):
    id_dict = {'strong':[], 'med':[], 'weak':[], 'strong_med':[], 'strong_weak':[], 'med_weak':[], 'all':[]}
    for sep_file in sep_files:
        intensity = sep_file.split('/')[-1]
        with open(sep_file, 'r') as f:
            for line in f:
                id = line.strip().split('\t')[0]
                id_dict[intensity].append(id)
    return id_dict

def get_combination_list():
    return ['strong', 'med', 'weak', 'strong_med', 'strong_weak', 'med_weak', 'all']

def make_result_dict(in_file, id_dict):
    result_dict = {'strong':[], 'med':[], 'weak':[], 'strong_med':[], 'strong_weak':[], 'med_weak':[], 'all':[]}
    with open(in_file, 'r') as f:
        for line in f:
            line = line.strip()
            id = line.split('\t')[0]
            combination_list = get_combination_list()
            for combination in combination_list:
                if id in id_dict[combination]:
                    result_dict[combination].append(line)
    return result_dict

def create_out_files(result_dict, out_dir):
    for intensity, lines in result_dict.items():
        with open(out_dir + intensity, 'w+') as f:
            for line in sorted(lines, key=lambda x: x.split('\t')[0]):
                f.write(line + '\n')

def sep_intensity():
    in_file, sep_files, out_dir = get_files()
    id_dict = make_id_dict(sep_files)
    result_dict = make_result_dict(in_file, id_dict)
    create_out_files(result_dict, out_dir)

if __name__ == '__main__':
    sep_intensity()
