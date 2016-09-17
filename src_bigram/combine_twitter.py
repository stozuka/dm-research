from os import listdir
from os.path import isfile, join
import json
import codecs
import re
import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')


# To detect URL
regex = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', re.IGNORECASE)

def process_ch():
	mypath = "Twitter/News"
	onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
	fullContent = ""
	bigTotal = 0

	for f in onlyfiles:
		f = join(mypath,f)
		print f
		if ".tw" in f:
			content_file = codecs.open(f,"r",encoding='utf-8')
					#content = content_file.read()

			count = 0
			for sentence in content_file:
				if len(sentence) > 0:
					sentence = regex.sub("" ,sentence)
					sentences = sentence.split("\t")
					count = count + 1
					if len(sentences) == 2:
						fullContent = fullContent + ' '.join(sentences[1].split()) + " "
						print "Tweet: ",sentences[1]
					else:
						fullContent = fullContent + ' '.join(sentences[0].split()) + " "
						print "Tweet: ",sentences[0]
					#u' '.join((agent_contact, agent_telno)).encode('utf-8').strip()
				print "Total ",count
			bigTotal = bigTotal + count
			
	print "Total all files ",bigTotal
	out = codecs.open("Twitter/News/all","w", "utf-8-sig")
	out.write(fullContent)
	out.close

def process_jp():
	mypath = "/Volumes/Transcend/Dropbox/workspace/NLTK/japanese/data_original/training"
	onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
	fullContent = ""
	bigTotal = 0

	for f in onlyfiles:
		f = join(mypath,f)
		print f
		if "._" not in f and "news" not in f:
			content_file = codecs.open(f,"r",encoding='utf-8')
					#content = content_file.read()

			count = 0
			for sentence in content_file:
				if len(sentence) > 0:
					sentence = regex.sub("" ,sentence)
					sentences = sentence.split("\t")
					count = count + 1
					if len(sentences) == 2:
						fullContent = fullContent + ' '.join(sentences[1].split()) + " "
						#print "Tweet: ",sentences[1]
					else:
						fullContent = fullContent + ' '.join(sentences[0].split()) + " "
						#print "Tweet: ",sentences[0]
					#u' '.join((agent_contact, agent_telno)).encode('utf-8').strip()
				#print "Total ",count
			bigTotal = bigTotal + count
		else:
			print "Ignoring %s"%f
			
	print "Total all files ",bigTotal
	out = codecs.open("/Volumes/Transcend/Dropbox/workspace/NLTK/japanese/all/all_emotions","w", "utf-8-sig")
	out.write(fullContent)
	out.close

process_jp()
