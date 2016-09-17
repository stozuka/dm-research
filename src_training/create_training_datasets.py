# -*- coding: utf-8 -*-
import glob

def file_io(original_file, out_file, ids_of_testing_tweets):
    try:
        with open(original_file, 'r') as original_f, open(out_file, 'w+') as out_f:
            original_line_counter = 0
            new_line_counter = 0
            print(original_file.split('/')[-1], 'processing...')
            for line in original_f:
                line = line.strip()
                text_id = line.split('\t')
                if text_id[-1] not in ids_of_testing_tweets:
                    out_f.write(text_id[0] + '\n')
                    new_line_counter += 1
                original_line_counter += 1
            print('Number of tweets rejected: ' + str(original_line_counter - new_line_counter))
    except FileNotFoundError as e:
        print(e)

def create_id_list(ids_file):
    ids_of_testing_tweets = []
    try:
        with open(ids_file, 'r') as ids_f:
            for line in ids_f:
                id = line.strip().split('\t')[1]
                ids_of_testing_tweets.append(id)
    except FileNotFoundError as e:
        print(e)
    return ids_of_testing_tweets

def create_out_file(ids_file, original_files, out_path):
    ids_of_testing_tweets = create_id_list(ids_file)
    print("Length of ids_of_testing_tweets: ", len(set(ids_of_testing_tweets)))
    for original_file in original_files:
        emotion = original_file.split('/')[-1].split('_')[-1]
        out_file = out_path + "training_" + emotion
        file_io(original_file, out_file, ids_of_testing_tweets)

if __name__ == '__main__':
    base_path = '/home/sadayuki/Dropbox/Data-Mining-Research/'
    ids_file = base_path + 'data_testing/manual_classification/combined_testing_data.txt'
    original_files  = glob.glob(base_path + '/data_original/rm_some_hashtags/*')
    out_path = base_path + 'data_training/'

    create_out_file(ids_file, original_files, out_path)

    print('Done.')
