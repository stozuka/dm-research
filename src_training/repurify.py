import keys
import re

def get_files():
    base_path = '/home/sadayuki/Dropbox/Data-Mining-Research/'
    in_file = base_path + 'data_evaluation/reduced_news/original/temp'
    out_file  = base_path + 'data_evaluation/reduced_news/original/temp'
    return in_file, out_file

def get_replace_dict():
    return {
        '「': '',
        '」': '',
        '【': '',
        '】': '',
        '[' : '',
        ']' : '',
        '（' : '',
        '）' : '',
        '『' : '',
        '』' : '',
        # '、' : '',
        # '。' : '',
        'http': ' http',
        '#': ' #'
    }

def get_processed_line(line):
    replaced_line = line
    for before, after in get_replace_dict().items():
        replaced_line = replaced_line.replace(before, after)

    http_removed = []
    for item in replaced_line.split(' '):
        if not item.startswith('http'):
            http_removed.append(item)

    return ' '.join(http_removed)

def create_out_file(processed, out_file):
    with open(out_file, 'w+') as out_f:
        for each in processed:
            out_f.write(each + '\n')

def get_purified_news():
    in_file, out_file = get_files()

    processed = []
    with open(in_file, 'r') as in_f:
        for line in in_f:
            line = line.strip()
            line = get_processed_line(line)
            processed.append(line)

    create_out_file(processed, out_file)

if __name__ == '__main__':
    get_purified_news()
