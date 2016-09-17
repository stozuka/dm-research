import re
import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

article = 'fucking tweet https://t.co/KoDWDUYPuA'
#print article
#article = re.sub(r'(?is)</html>.+', '</html>', article)
#article = re.sub(u'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'\".,<>?]))', 'url', article)
regex = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', re.IGNORECASE)
line = regex.sub("" ,article)
#print line

def my_range(start, end, step):
    while start < end:
        yield start
        start += step

#for x in my_range(0, 4, 2):
#    print x
import unicodedata, re
import codecs

'''all_chars = (unichr(i) for i in xrange(0x110000))
control_chars = ''.join(c for c in all_chars if unicodedata.category(c) == 'Cc')
# or equivalently and much more efficiently
control_chars = ''.join(map(unichr, range(0,32) + range(127,160)))

control_char_re = re.compile('[%s]' % re.escape(control_chars))

def remove_control_chars(s):
    return control_char_re.sub('', s)'''

def remove_control_characters(s):
    return "".join(ch for ch in s if unicodedata.category(ch)[0]!="C")

def load( path):
    words = {}
    f = codecs.open(path,"r", "utf-8")
    for word in f:
    	word = remove_control_characters(word)
    	print word
        words[word.strip()] = word.strip()
    print "Loaded %s words"%str(len(words))
    return words


words = load("patterns/patterns_test")
out = codecs.open("patterns/patterns_test_clean","w", "utf-8-sig")
for pattern in words:
	out.write(pattern+"\n")
out.close()
