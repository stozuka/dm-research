# -*- coding: utf-8 -*-
import MeCab

result = []

text = '2,400円'
mecab_tagger = MeCab.Tagger("-Ochasen")
mecab_tagger.parse('')
node = mecab_tagger.parseToNode(text)

while node:
    result.append(node.surface)
    node = node.next

print(result)
