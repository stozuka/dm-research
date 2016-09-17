# -*- coding: utf-8 -*-
import re

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
    in_file = "/home/sadayuki/Dropbox/Data-Mining-Research/Preprocessing/news.txt"
    file = open(in_file, "r")

    lines = ""

    for line in file:
        lines += replace(line.split()) + "\n"

    lines = lines.strip()

    print(lines)
