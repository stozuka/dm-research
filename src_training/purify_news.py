import keys


def get_files():
    base_path = '/home/sadayuki/Dropbox/Data-Mining-Research/'
    in_file = base_path + 'data_evaluation/reduced_news/original/all_51871'
    out_file  = base_path + 'data_evaluation/reduced_news/original/temp'
    return in_file, out_file

def get_emo_word_list():
    return keys.OPINIONATED_KEYWORDS.split()

def is_contain_emo(line):
    emo_word_list = get_emo_word_list()
    for emo_word in emo_word_list:
        if emo_word in line:
            return True
    return False

def create_out_file(purified_list, out_file):
    with open(out_file, 'w+') as out_f:
        for line in purified_list:
            out_f.write(line + '\n')

def get_purified_news():
    in_file, out_file = get_files()
    original_len = 0
    purified_list = []

    with open(in_file, 'r') as in_f:
        for line in in_f:
            original_len += 1
            line = line.strip()
            if not is_contain_emo(line):
                purified_list.append(line)

    print('Original len:', original_len, sep='\t')
    print('After purified:', len(purified_list), sep='\t')

    create_out_file(purified_list, out_file)

if __name__ == '__main__':
    get_purified_news()
