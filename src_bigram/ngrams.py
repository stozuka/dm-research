from nltk.util import ngrams
from nltk import bigrams
import nltk
import json
import codecs
import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

def weightedBigrams(path,mode):
    edges = {}
    with codecs.open(path,"r", "utf-8") as content_file:
        content = content_file.read()

    #mode 1 json
    #mode 2 plain
    if mode == 1:
        jsonContent = json.loads(content)
        fullContent = ""
        for sentence in jsonContent:
        	fullContent = fullContent + ' '.join(sentence.split()) + " "
    else:
        fullContent = content

    print fullContent,type(fullContent)

    n_grams = bigrams(fullContent)
    #for grams in n_grams:
     # print grams


    fdist = nltk.FreqDist(n_grams)

    print len(fdist)
    out = codecs.open(path+"_edges","w", "utf-8-sig")
    maxi = 0.0
    foundMax = 0
    for k,v in fdist.most_common(len(fdist)): #fdist.items():
        #print "'%s' - '%s' : %d"%(k[0],k[1],v)
        if len(k[0]) != 0 and len(k[1]) != 0:
            # replace white space by a special mark
            if k[0] == " ":
                w1 = "_blank_"
            else:
                w1 = k[0]
            if k[1] == " ":
                w2 = "_blank_"
            else:
                w2 = k[1]
        	if not foundMax:
        		foundMax = 1
        		maxi = float(v)
        	#print "%s -> %s : %d - %f"%(k[0],k[1],v, float(v)/float(maxi))
            	out.write("%s -> %s : %d - %f"%(k[0],k[1],v, float(v)/float(maxi)))
                out.write("\n")
                edges["%s %s"%(w1,w2)]=float(v)/float(maxi)
    out.close
    return edges;
