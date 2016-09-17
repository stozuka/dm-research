

def get_files():
    base_path = '/home/sadayuki/Dropbox/Data-Mining-Research/'
    manual_file = base_path + 'data_intensity/intensity_converted/score'
    out_dir = base_path + 'data_intensity/sep_score/manual_classification/'
    return manual_file, out_dir

def get_intensity_list(line):
    result = {}
    emo_list = line.strip().split('\t')[-1].split()
    for each in emo_list:
        intensity = each.strip().split(':')[-1]
        result[intensity] = result.get(intensity, 0) + 1
    return result

def check_category(line):
    intensity_dict = get_intensity_list(line)
    if 'strong' in intensity_dict and 'med' in intensity_dict and 'weak' in intensity_dict:
        return 'all'
    elif 'strong' in intensity_dict and 'med' in intensity_dict:
        return 'strong_med'
    elif 'strong' in intensity_dict and 'weak' in intensity_dict:
        return 'strong_weak'
    elif 'med' in intensity_dict and 'weak' in intensity_dict:
        return 'med_weak'
    elif 'strong' in intensity_dict:
        return 'strong'
    elif 'med' in intensity_dict:
        return 'med'
    elif 'weak' in intensity_dict:
        return 'weak'
    else:
        print('Something is wrong!')

def print_stats(result_dict, out_dir):
    out_file = '/'.join(out_dir.split('/')[:-3]) + '/sep_stats/score'
    with open(out_file, 'w+') as f:
        for intensity, tweets in sorted(result_dict.items(), key=lambda x: len(x[1]), reverse=True):
            num = len(tweets)
            print(intensity, ':', num)
            f.write(intensity + ':' + str(num) + '\n')

def create_out_file(result_dict, out_dir):
    for intensity, lines in result_dict.items():
        out_file = out_dir + intensity
        with open(out_file, 'w+') as f:
            for line in lines:
                f.write(line + '\n')

def sep_intensity():
    in_file, out_dir = get_files()
    result_dict = {'strong':[], 'med':[], 'weak':[], 'strong_med':[], 'strong_weak':[], 'med_weak':[], 'all':[]}

    with open(in_file, 'r') as in_f:
        for line in in_f:
            line = line.strip()
            category = check_category(line)
            result_dict[category].append(line)

    print_stats(result_dict, out_dir)
    create_out_file(result_dict, out_dir)

if __name__ == '__main__':
    sep_intensity()
