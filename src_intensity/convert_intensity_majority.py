

def get_files():
    base_path = '/home/sadayuki/Dropbox/Data-Mining-Research/'
    in_file = base_path + 'data_intensity/rm_only_one_person_emo/rm_only_one_person_emo'
    out_file = base_path + 'data_intensity/intensity_converted/intensity_converted'
    return in_file, out_file

def check_category(score_dict):
    if score_dict['3'] >= 2:
        return 'strong'
    elif score_dict['2'] >= 2:
        return 'med'
    elif score_dict['1'] >= 2:
        return 'weak'
    elif score_dict['3'] == 1 and score_dict['2'] == 1 and score_dict['1'] == 1:
        return 'med'
    elif score_dict['3'] == 1 and score_dict['2'] == 1 and score_dict['0'] == 1:
        return 'med'
    elif score_dict['3'] == 1 and score_dict['1'] == 1 and score_dict['0'] == 1:
        return 'weak'
    elif score_dict['2'] == 1 and score_dict['1'] == 1 and score_dict['0'] == 1:
        return 'weak'
    else:
        print('Something wrong!')

def get_category(intensity):
    score_dict = {'3':0, '2':0, '1':0, '0':0}
    for score in intensity:
        score_dict[score] = score_dict.get(score, 0) + 1
    return check_category(score_dict)

def convert_emos(emos):
    result = {}
    for emo in emos:
        name, intensity = emo.split(':')
        intensity = intensity.split()
        category = get_category(intensity)
        result[name] = category
    return result

def create_out_file(result, out_file):
    with open(out_file, 'w+') as f:
        for tweet in result:
            id, text, emos = tweet
            f.write(id + '\t' + text + '\t')
            for emo, intensity in emos.items():
                f.write(emo + ':' + intensity + ' ')
            f.write('\n')

def convert_intensity():
    in_file, out_file = get_files()
    result = []

    with open(in_file, 'r') as in_f:
        for line in in_f:
            line = line.strip().split('\t')
            id, text, *emos = line
            converted_emos = convert_emos(emos)
            result.append([id, text, converted_emos])

    create_out_file(result, out_file)

if __name__ == '__main__':
    convert_intensity()
