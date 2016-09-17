from ngrams import weightedBigrams
import operator
import codecs
import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

def minusNetworks(subjPath, objPath):
	print "Processing ",subjPath

    	# Get edges for the subjective graph
    	edges1 = weightedBigrams(subjPath,2)
        '''print "subjective"
        for edge in edges1:
            print "%s %f"%(edge,edges1[edge])'''

        # Get edges for the objective graph
        edges2 = weightedBigrams(objPath,2)
        '''print "objective"
        for edge in edges2:
            print "%s %f"%(edge,edges2[edge])'''

        diffTh = 0.0;
        edges = {}
        droped = {}
        for edge in edges1:
            if edge in edges2:
                value = edges1[edge] - edges2[edge] 
                if(value >= diffTh):
                    edges[edge] = value
                else:
                    #print "Drop this shared edge %s: %f"%(edge,value)
                    droped[edge] = value
            else:
                if edges1[edge] >= diffTh:
                    edges[edge] = edges1[edge]
                else:
                    #print "Drop this unique edge %s: %f"%(edge,edges1[edge])
                    droped[edge] = edges1[edge]
        

        sorted_edges = sorted(edges.items(), key=operator.itemgetter(1), reverse=True)
        out = codecs.open("/Volumes/Transcend/Dropbox/workspace/NLTK/japanese/networks/subjective","w", "utf-8-sig")
        words = {}
        netEdges = {}
        countWords = 0
        for (edge, value) in sorted_edges:
            print "%s\t%f"%(edge,value)
            tokens = edge.split(" ")
            if tokens[0] not in words:
                countWords = countWords + 1
                words[tokens[0]] = countWords
            if tokens[1] not in words:
                countWords = countWords + 1
                words[tokens[1]] = countWords
            netEdge = unicode(words[tokens[0]]) + " " + unicode(words[tokens[1]])
            netEdges[netEdge] = value

            out.write("%s\t%f\n"%(edge,value))
        out.close

        out = codecs.open("/Volumes/Transcend/Dropbox/workspace/NLTK/japanese/networks/dropped","w", "utf-8-sig")
        sorted_droped = sorted(droped.items(), key=operator.itemgetter(1))
        for (edge, value) in sorted_droped:
            print "%s\t%f"%(edge,value)
            out.write("%s\t%f\n"%(edge,value))
        out.close

        saveNetwork(words,netEdges)

#def processTweets(path):


#def tokenize:

def saveNetwork(words, edges):
        out = codecs.open("/Volumes/Transcend/Dropbox/workspace/NLTK/japanese/networks/minused.net","w", "utf-8-sig")
        out2 = codecs.open("/Volumes/Transcend/Dropbox/workspace/NLTK/japanese/networks/minused.vertices","w", "utf-8-sig")
        out3 = codecs.open("/Volumes/Transcend/Dropbox/workspace/NLTK/japanese/networks/minused.edges","w", "utf-8-sig")
        #Write the vertices names
        out.write("*Vertices "+ unicode(len(words)) + "\n")
            
        sorted_words = sorted(words.items(), key=operator.itemgetter(1))
        for (word, value) in sorted_words:
            line = unicode(value) + " \"" + word + "\" 0.0 0.0 0.0";

            out.write(line+"\n");
            out2.write(unicode(value) + " " + word+"\n")
        #Write the Edges
        out.write("*Arcs \n");
        sorted_edges = sorted(edges.items(), key=operator.itemgetter(1), reverse=True)
        for (edge, value) in sorted_edges:
           
           out.write(edge + " " + unicode(value)+"\n");
           out3.write(edge + " " + unicode(value)+"\n")
        out.close();
        out2.close()
        out3.close()


def replaceWordByTag(word):

        # If HT
        if word[0] == '#':
            word = "<hashtag>";
        

        #If URL
        if "http" in word or "https" in word:
            word = "<url>";
        

        #If mini URL
        if len(word) > 3 and "co/" in word[0, 3]:
            word = "<minurl>";


        #If user mention
        if word[0] == '@':
            word = "<usermention>";
        

        return word;

def removeLatinChars(path):
    f = codecs.open(path,"r", "utf-8")
    out = codecs.open(path+"_nolatin","w", "utf-8-sig")

    for line in f:
        import re
        if re.search('[a-zA-Z]', line):
            print "skip %s"%line
        else:
            out.write(line)
    out.close()



def getUnigramsByMetric(net_file, metricCol, th, out):

    out = codecs.open(out,"w", "utf-8-sig")

    f = codecs.open(net_file,"r", "utf-8")

    for line in f:
        if "degree" in line:
            continue

        tokens = line.split("\t")

        if float(tokens[metricCol]) >= th:
            print line
            out.write(tokens[0]+"\t"+tokens[1]+"\t"+tokens[metricCol]+"\n")

    out.close()


def findEmotionWords(pathEdges, pathNodes, pathPWs, out):
    out = codecs.open(out,"w", "utf-8-sig")

    f1 = codecs.open(pathEdges,"r", "utf-8")
    f2 = codecs.open(pathNodes,"r", "utf-8")
    f3 = codecs.open(pathPWs,"r", "utf-8")

    #Read the edges
    edges = []
    for line in f1:
        edges.append(line)

    #Read the nodes
    nodes = {}
    for line in f2:
        #print line
        tokens = line.split(" ")
        nodes[tokens[0]] = tokens[1].strip()


    for line in f3:
        tokens = line.split("\t")
        index = tokens[0]
        word = tokens[1]
        print line
        for edge in edges:
            tokens = edge.split(" ")
            index1 = tokens[0]
            index2 = tokens[1]
            value = tokens[2].strip()
            if index1 in nodes and index2 in nodes:
                if index1 == index or index2 == index:
                    if float(value) > 0.0001:
                        print word+": "+nodes[index1]+nodes[index2]+" - "+value
                        out.write(nodes[index1]+nodes[index2]+"\t"+value+"\n")
    out.close()


#findEmotionWords("network/dropped","network/pws")
#minusNetworks("Murmur/total/all", "Twitter/News/all")
#minusNetworks("/Volumes/Transcend/Dropbox/workspace/NLTK/japanese/all/all_emotions", "/Volumes/Transcend/Dropbox/workspace/NLTK/japanese/data_original/training/training_news")
#minusNetworks("Murmur/total/moods/angry.json", "")
#getUnigramsByMetric("/Volumes/Transcend/Dropbox/workspace/NLTK/japanese/networks/minused [Nodes].csv", 6, 0.25,"/Volumes/Transcend/Dropbox/workspace/NLTK/japanese/networks/words/pws")

#findEmotionWords("/Volumes/Transcend/Dropbox/workspace/NLTK/japanese/networks/minused.edges","/Volumes/Transcend/Dropbox/workspace/NLTK/japanese/networks/minused.vertices","/Volumes/Transcend/Dropbox/workspace/NLTK/japanese/networks/words/pws","/Volumes/Transcend/Dropbox/workspace/NLTK/japanese/networks/words/pws_bi")
removeLatinChars("/Volumes/Transcend/Dropbox/workspace/NLTK/japanese/networks/words/pws_bi")


