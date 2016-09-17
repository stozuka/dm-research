

def get_files():
    base_path = '/home/sadayuki/Dropbox/Data-Mining-Research/'
    in_file = base_path + 'data_intensity/rm_only_one_person_emo/rm_only_one_person_emo'
    out_file = base_path + 'data_intensity/intensity_converted/score'
    return in_file, out_file

def check_category(total_score):
    if total_score > 6:
        return 'strong'
    elif total_score > 3:
        return 'med'
    else:
        return 'weak'

def get_category(intensity):
    total_score = 0
    for score in intensity:
        total_score += int(score)
    return check_category(total_score)

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
