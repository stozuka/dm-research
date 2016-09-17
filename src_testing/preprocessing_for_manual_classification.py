# -*- coding: utf-8 -*-
import re
import os
import random

def separate_hashtag(text):
    text = text.replace("#", " #")
    return text

def is_starts_with_hashtag(item):
    pattern = r"\#"
    return re.match(pattern, item)

def is_starts_with_url(item):
    pattern = r"http"
    return re.match(pattern, item)

def is_starts_with_at(item):
    pattern = r"@"
    return re.match(pattern, item)

def is_starts_with_text(item):
    if is_starts_with_hashtag(item) or is_starts_with_at(item) or is_starts_with_url(item):
        return False
    else:
        return True

def replace(line_array):
    replaced_line = []
    for word in line_array:
        if is_starts_with_hashtag(word):
            replaced_line.append('<hashtag>')
        elif is_starts_with_url(word):
            replaced_line.append('<url>')
        elif is_starts_with_at(word):
            replaced_line.append('<usermention>')
        else:
            replaced_line.append(word)
    return " ".join(replaced_line)

if __name__ == '__main__':
    base_path = "/home/sadayuki/Dropbox/Data-Mining-Research/data_testing/manual_classification/"
    in_file = base_path + "shuffled_combined_testing_data.txt"
    out_file = base_path + "processed_testing"

    replaced_text_id = []

    with open(in_file, "r") as in_f, open(out_file, "w+") as out_f:
        header = "ツイート ID 恍惚(3)/喜び(2)/安らぎ(1) 敬愛(3)/信頼(2)/容認(1) 恐怖(3)/心配(2)/不安(1) 驚愕(3)/驚き(2)/動揺(1) 悲嘆(3)/悲しみ(2)/感傷的(1) 憎悪(3)/嫌悪感(2)/倦怠(1) 激怒(3)/怒り(2)/苛立ち(1) 警戒(3)/期待・予測(2)/関心(1)"
        emotion_score = "0 0 0 0 0 0 0 0"

        out_f.write("\t".join(header.split()) + "\n")

        for line in in_f:
            text, id = line.strip().split("\t")
            text = replace(text.split())
            out_f.write(text + "\t" + id + "\t" + "\t".join(emotion_score.split()) + "\n")

    # # Use this part to get ids
    # ids = []
    # for item in replaced_text_id:
    #     ids.append(item[1].strip())
    # ids.sort()
    # list(set(ids))
    # for id in ids:
    #     print(id)

    # Use this part to get randamized texts and ids
    # for i in range(0, 100):
    #     random.shuffle(replaced_text_id)
