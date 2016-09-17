# -*- coding: utf-8 -*-

if __name__ == '__main__':
    in_file = '/home/sadayuki/Dropbox/Data-Mining-Research/data_testing/manual_classification/combined_testing_data.txt'

    ids = []
    is_contain_dup = False
    
    with open(in_file, 'r') as in_f:
        for line in in_f:
            id = line.split('\t')[1]
            if id not in ids:
                ids.append(id)
            else:
                is_contain_dup = True
                print('Duplicate ID:', id)

    if is_contain_dup:
        print('Contains duplicated tweets.')
    else:
        print('No duplicated tweets.')