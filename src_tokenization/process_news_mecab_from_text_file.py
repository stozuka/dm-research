# -*- coding: utf-8 -*-
import re
import sys
import MeCab
import mojimoji
import keys

def separate_url_and_hashtag(text):
    text = text.replace("。http", "。 http")
    text = text.replace("。#", "。 #")
    text = text.replace("、#", "、 #")
    text = text.replace("・#", "・ #")
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

def MeCabMorpho(word_list):
    result = []
    for word in word_list:
        if is_starts_with_text(word):
            mecab_tagger = MeCab.Tagger("-Ochasen")
            mecab_tagger.parse('')
            node = mecab_tagger.parseToNode(word)
            while node:
                result.append(node.surface)
                node = node.next
        else:
            result.append(word)
    return result

def combine_non_ja_chars(word_list):
    result = []
    non_japanese_str = ""
    pattern = r'[一-龠ぁ-んァ-ヶ【】「」、。]'

    for char in word_list:
        if is_starts_with_text(char):
            if re.match(pattern, char): # If Japanese character
                if non_japanese_str != "":
                    result.append(non_japanese_str)
                    non_japanese_str = ""
                result.append(char)
            else: # If not Japanese character
                non_japanese_str = non_japanese_str + char
        else: # If start with #, @ or http.
            if non_japanese_str != "":
                result.append(non_japanese_str)
                non_japanese_str = ""
            result.append(char)

    if not non_japanese_str == "":
        result.append(non_japanese_str)

    return result

def preprocessing(in_file):
    processed_texts = []
    for line in in_file:
        # text is a string
        text = line.strip().split('\t')[0]
        text = mojimoji.zen_to_han(text, kana=False)
        text = separate_url_and_hashtag(text)

        # word_list is a list
        word_list = text.split()
        word_list = MeCabMorpho(word_list)
        word_list = combine_non_ja_chars(word_list)
        processed_texts.append(word_list)
    return processed_texts

def replace(processed_text):
    original_line = processed_text
    replaced_line = []
    for word in original_line:
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
    # EMOTION = sys.argv[1]
    data_path = "/home/sadayuki/Dropbox/Data-Mining-Research/data_evaluation/reduced_news/"
    in_file = data_path + "original/temp"
    out_file = data_path + "tokenized/temp"

    processed_texts = ""

    with open(in_file, mode="r") as in_file:
        processed_texts = preprocessing(in_file)

    with open(out_file, mode="w+") as out_file:
        for processed_text in processed_texts:
            text = replace(processed_text)
            out_file.write(text + "\n")
