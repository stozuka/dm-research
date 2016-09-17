# -*- coding: utf-8 -*-
import re
import csv
from operator import itemgetter
import MeCab

def read_file(dir_name, in_file_name):
    data_array = []

    with open(dir_name + in_file_name, mode="r", encoding='utf-8') as in_file:
        data_dict = csv.DictReader(in_file, delimiter="\t")
        for doc in data_dict:
            data_array.append(doc)

    return data_array[1000:1050]

def add_pos_info(data_array):
    result = []
    tagger = MeCab.Tagger('-Ochasen')

    for item in data_array:
        mecab_result = tagger.parse(item["label"])
        pos = mecab_result.split()[3]
        item["pos"] = pos
        result.append(item)

    return result

# TODO implement this function!!!
def add_pw_score(data_array):
    return data_array

def add_pos_info_and_pw_score(data_array):
    result = []

    result = add_pos_info(data_array)
    result = add_pw_score(data_array)

    return result

def get_measurement(measurement_number):
    MEASUREMENTS = {
        1: "clustering",
        2: "triangles",
        3: "eigencentrality",
        4: "degree",
        5: "eccentricity",
        6: "closnesscentrality",
        7: "harmonicclosnesscentrality",
        8: "betweenesscentrality"
    }
    return MEASUREMENTS[measurement_number]

def sort_by_score(data_array, measurement):
    data_array = sorted(
        data_array,
        key=itemgetter(measurement),
        reverse=True
    )
    return data_array

def create_sorted_score_list(data_array, measurement):
    score_list = []

    for item in data_array:
        score_list.append(item[measurement])
    score_list = sorted(list(set(score_list)), reverse=True)

    print("Length of array: ", len(data_array))
    print("Lenght of set  : ", len(score_list))
    print("Removed        : ", len(data_array) - len(score_list))

    return  score_list

def write_ranking_into_dict(data_array, score_list, measurement):
    result = []

    for item in data_array:
        for i, score in enumerate(score_list):
            if item[measurement] == score:
                item[measurement + "_ranking"] = i + 1;
        result.append(item)

    return result

def add_ranking(data_array, measurement_number=1):
    result = []
    score_list = []
    measurement = get_measurement(measurement_number) # measurement in string

    data_array = sort_by_score(data_array, measurement)
    score_list = create_sorted_score_list(data_array, measurement)
    result = write_ranking_into_dict(data_array, score_list, measurement)

    return result

if __name__ == '__main__':
    # ATTENTION: change measurement_number
    # 1: "clustering", 2: "triangles",    3: "eigencentrality",
    # 4: "degree",     5: "eccentricity", 6: "closnesscentrality",
    # 7: "harmonicclosnesscentrality",    8: "betweenesscentrality"
    measurement_number = 1

    dir_name = "/home/sadayuki/Research-Local/Data-Mining-Research/Data/with_tokenizer/PW-score/"
    in_file_name = "minused_results.csv"

    data_array = read_file(dir_name, in_file_name)
    data_array = add_pos_info_and_pw_score(data_array)
    data_array = add_ranking(data_array, measurement_number)

    for item in data_array:
        print(item["label"], item["clustering"], item["clustering_ranking"])
