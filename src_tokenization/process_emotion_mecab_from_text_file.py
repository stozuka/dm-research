# -*- coding: utf-8 -*-
import re
import os
import sys
import MeCab
import mojimoji
import keys

def separate_punct(text):
    replaced_text = text
    replace_dict = {
        "〜": " 〜 ",
        "~": " ~ ",
        "～": " ～ ",
        "・": " ・ ",
        "。": " 。 ",
        "、": " 、 ",
        "!": " ! ",
        "?": " ? ",
        "！": " ！ ",
        "？": " ？ ",
        "「": " 「 ",
        "」": " 」 ",
        "『": " 『 ",
        "』": " 』 ",
        "【": " 【 ",
        "】": " 】 ",
        "［": " ［ ",
        "］": " ］ "
    }
    for key, value in replace_dict.items():
        replaced_text = replaced_text.replace(key, value)
    return replaced_text

def extract_usermention(segment):
    pat = r"@[A-Za-z0-9_]+"
    match = re.search(pat, segment)
    if match != None:
        start_pos = match.start()
        end_pos = match.end()
        segment = segment[0:start_pos] + ' ' + match.group() + ' ' + segment[end_pos:]
        return segment
    else:
        return segment

def separate_usermention(text):
    processed_word_list = []
    word_list = text.split()
    for segment in word_list:
        if is_starts_with_text(segment):
            segment = extract_usermention(segment)
            processed_word_list.append(segment)
        else:
            processed_word_list.append(segment)
    return " ".join(processed_word_list)

def separation(text):
    text = separate_punct(text)
    text = separate_usermention(text)
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

def mecab_morph(word_list):
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

def combine_num_and_eng(word_list):
    result = []
    num_pat = r'^[0-9]+(,[0-9]+)?$'
    eng_pat = r'^[a-zA-Z]+$'
    num_str = ""

    for index, char in enumerate(word_list):
        if char == "":
            continue

        if index == 0:
            result.append(char)
            continue

        if re.match(num_pat, char): # If number, put is in num_str
            num_str += char
        elif re.match(eng_pat, char) and num_str != "": # If number + English, make it as one item
            num_str += char
            result.append(num_str)
            num_str = ""
        else: # If not the combination above
            if num_str != "":
                result.append(num_str)
                num_str = ""
            result.append(char)

    if num_str != "":
        result.append(num_str)

    return result

def combine_punct(word_list):
    result = []
    punct_pat = r'^[〜~～。、・！？!?,.。、…]+$'
    punct_str = ""

    for index, char in enumerate(word_list):
        if index == 0:
            result.append(char)
            continue

        if re.match(punct_pat, char):
            punct_str += char
        else:
            if punct_str != "":
                result.append(punct_str)
                punct_str = ""
            result.append(char)

    if punct_str != "":
        result.append(punct_str)

    return result

def combine_emoticons(word_list):
    result = []
    pattern_non_emoticon = r'[a-zA-Z]{2,}|[一-龠ぁ-んァ-ヶ0-9。、ー〜~～！？!?…・\,\.]'
    emoticon_str = ""

    for char in word_list:
        if is_starts_with_text(char):
            if re.match(pattern_non_emoticon, char) != None: # If not a part of emoticon
                if emoticon_str != "":
                    result.append(emoticon_str)
                    emoticon_str = ""
                result.append(char)
            else: # If a part of emoticon
                emoticon_str += char
        else: # If start with #, @, http or others
            if emoticon_str != "":
                result.append(emoticon_str)
                emoticon_str = ""
            result.append(char)

    if emoticon_str != "":
        result.append(emoticon_str)

    return result

def combine(word_list):
    combined_word_list = word_list
    combined_word_list = combine_num_and_eng(combined_word_list)
    combined_word_list = combine_punct(combined_word_list)
    combined_word_list = combine_emoticons(combined_word_list)
    return combined_word_list

def preprocessing(in_file):
    text_list = []
    processed_texts = []

    # Remove IDs
    for line in in_file:
        text_list.append(line.split("\t")[0].strip())

    for text in text_list:
        # text is a string
        text = text.lower()
        text = mojimoji.zen_to_han(text, kana=False)
        text = separation(text)
        # word_list is a list
        word_list = text.split()
        word_list = mecab_morph(word_list)
        word_list = combine(word_list)
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
    EMOTION = sys.argv[1]
    data_path = "/home/sadayuki/Dropbox/Data-Mining-Research/data_testing/"
    in_file = data_path + "final_50/final_50_" + EMOTION
    out_file = data_path + "tokenized/testing_" + EMOTION

    processed_texts = ""

    with open(in_file, mode="r") as in_file:
        processed_texts = preprocessing(in_file)

    with open(out_file, mode="w+") as out_file:
        for processed_text in processed_texts:
            text = replace(processed_text)
            out_file.write(text + "\n")
