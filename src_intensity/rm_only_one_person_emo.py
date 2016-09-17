

def get_files():
    base_path = '/home/sadayuki/Dropbox/Data-Mining-Research/'
    in_file = base_path + 'data_intensity/rm_none/rm_none'
    out_file = base_path + 'data_intensity/rm_only_one_person_emo/rm_only_one_person_emo'
    return in_file, out_file

def get_zero_count(emo_strength):
    zero_count = 0
    for each_strength in emo_strength:
        if int(each_strength) == 0:
            zero_count += 1
    return zero_count

def reduce_emos(emos):
    result = []
    for emo in emos:
        emo = emo.strip().split()
        # emo_strength looks, ['2', '2', '2']
        emo_name, emo_strength = emo[0], emo[1:]
        zero_count = get_zero_count(emo_strength)
        if zero_count <= 1:
            result.append([emo_name, emo_strength])
    return result

def calc_mean(original):
    result = []
    for tweet in original:
        emo_dict = {}
        for emos in tweet[2]:
            total = 0
            for score in emos[1]:
                total += float(score)
            mean = total / 3
            strength = ''
            if mean >= 2.2:
                strength = '1' # 1 is strong
            else:
                strength = '0' # 0 is weak
            emo_dict[emos[0]] = strength
        result.append([tweet[0], tweet[1], emo_dict])
    return result

def create_out_file(result, out_f):
    for tweet in result:
        # print(tweet[0], tweet[1])
        out_f.write(tweet[0] + '\t' + tweet[1] + '\t')
        for emo, strength in tweet[2]:
            out_f.write(emo + ':')
            for each in strength:
                out_f.write(each + ' ')
            out_f.write('\t')
        out_f.write('\n')

def rm_only_one_person_emo():
    in_file, out_file = get_files()
    result = []
    with open(in_file, 'r') as in_f:
        for line in in_f:
            line = line.strip().split('\t')
            id, text, emos = line[0], line[1], line[2:]
            # emos looks, ['anticipation 1 0 1', 'disgust 0 0 0', ...]
            reduced_emos = reduce_emos(emos)
            result.append([id, text, reduced_emos])

    # result = calc_mean(result)

    with open(out_file, 'w+') as out_f:
        create_out_file(result, out_f)

if __name__ == '__main__':
    rm_only_one_person_emo()
