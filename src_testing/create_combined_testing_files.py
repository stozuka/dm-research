# -*- coding: utf-8 -*-
import os
import glob

def create_combined_testing_file(in_path, out_path):
    final_50_files = glob.glob(in_path)

    count = 0 # To check if there are exactly 50 tweets for each emotion.
    with open(out_path, mode="w+") as out_file:
        for final_50_file in final_50_files:
            with open(final_50_file, mode="r") as in_file:
                for line in in_file:
                    count += 1
                    out_file.write(line.strip() + "\n")
                print(final_50_file.split("/")[-1], count)
                count = 0

if __name__ == '__main__':
    data_path = "/home/sadayuki/Dropbox/Data-Mining-Research/data_testing/"
    in_path = data_path + "final_50/*"
    out_path = data_path + "manual_classification/combined_testing_data.txt"

    create_combined_testing_file(in_path, out_path)
