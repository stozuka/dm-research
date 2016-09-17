# -*- coding: utf-8 -*-
import sys
import mojimoji

def mojimoji_processing(in_file):
    mojimojied_text = []
    for line in in_file:
        text = line.strip().split("\t")[0].lower()
        mojimojied_text.append(mojimoji.zen_to_han(text, kana=False))
    return mojimojied_text

if __name__ == '__main__':
    EMOTION = sys.argv[1]
    data_path = "/home/sadayuki/Dropbox/Data-Mining-Research/data_testing/"

    # in_file = data_path + "final_50/final_50_" + EMOTION # For emotion
    in_file = data_path + "original_after_rm_dup/original_" + EMOTION # For news

    out_file = data_path + "mojimojied/mojimojied_" + EMOTION

    mojimojied_text = []

    with open(in_file, mode="r") as in_file:
        mojimojied_text = mojimoji_processing(in_file)

    with open(out_file, mode="w+") as out_file:
        for text in mojimojied_text:
            out_file.write(text + "\n")
