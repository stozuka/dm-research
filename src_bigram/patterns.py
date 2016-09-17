from nltk.util import ngrams
import nltk
import codecs
import unicodedata
import operator
import re
import json
from os import listdir
from os.path import isfile, join
import sys
from multiprocessing import Process

reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

def remove_control_characters(s):
    return u"".join(ch for ch in s if unicodedata.category(ch)[0]!="C")

def my_range(start, end, step):
    while start < end:
        yield start
        start += step

def load( path):
    words = {}
    f = codecs.open(path,"r", "utf-8")
    for word in f:
        word = word.split("\t")[0]
        word = remove_control_characters(word)
        words[word.strip()] = word.strip()
    print "Loaded %s words"%str(len(words))
    return words


def getInstances(meta_pattern):
    
    pwsPath = "/Volumes/Transcend/Dropbox/workspace/NLTK/japanese/networks/words/pws_bi_nolatin";
    hwsPath = "/Volumes/Transcend/Dropbox/workspace/NLTK/japanese/networks/words/hws_bi_nolatin";
    #path = "Murmur/total/all";
    path = "/Volumes/Transcend/Dropbox/workspace/NLTK/japanese/all/all_emotions"


    hws = {}
    pws = {}
    ws = {}
    hws = load(hwsPath)
    pws = load(pwsPath)
    #for hw in hws:
    #    print hw
    #print hws
    #print pws

    instances = {}

    pattTokens = meta_pattern.split("_");
    W = len(pattTokens)
    print pattTokens
    print W

    # Read all the subjective data 
    with codecs.open(path,"r", "utf-8") as content_file:
       	content = content_file.read()

    # Get all the unigrams
    n = 2
    #tokens = nltk.word_tokenize(content)
    onegrams = ngrams(content, n)
    tokens = []
    for grams in onegrams:
        if grams[0] == " ":
            w1 = u"_blank_"
        else:
            w1 = remove_control_characters(grams[0])
        if grams[1] == " ":
            w2 = u"_blank_"
        else:
            w2 = remove_control_characters(grams[1])
        tokens.append(w1.strip()+w2.strip())

    #print tokens
    #for token in tokens:
      #  print token
    for i in range(1, (len(tokens) - W) + 1):
        pattern = u"";
        for j in range( 0, W):
        #for j in my_range(0,W,2):
            current = i + j;
            token = remove_control_characters(tokens[current]);
            #print token
            #print pattTokens[j]
            if "hw" in pattTokens[j]:
                ws = hws;
                #print pattTokens[j]+" CW"        
            else :
                ws = pws;
                #print pattTokens[j]+" HW"
            if token in ws:
                
                #print "Match "+token;
                pattern = pattern + token;
            else:
                break
                
            if ((j + 1) == W):
                pattern = remove_control_characters(pattern.strip());
                #print "pattern "+pattern    

                if pattern not in instances:
                    instances[pattern] = 1
                else:
                    instances[pattern] = instances[pattern] + 1

    out = codecs.open("/Volumes/Transcend/Dropbox/workspace/NLTK/japanese/instances/"+meta_pattern,"w", "utf-8-sig")
    sorted_instances = sorted(instances.items(), key=operator.itemgetter(1), reverse=True)
    for (instance, value) in sorted_instances:
           print instance
           if W == 3:
                realInstance = instance[0:2] + instance[4:6]
           if W == 2:
                if len(instance) == 4:
                    realInstance = instance[0:2] + instance[3]
                else:
                    realInstance = instance[0:2]
           out.write(remove_control_characters(realInstance) + u"\t" + remove_control_characters(instance) + u"\t" + unicode(value)+u"\n");
    out.close()

def regexReservedWords(token):
    newToken = u"";
    tokens = list(token)
    for token in tokens:  
        # Includes the *
        #if re.match(r'(\^|\$|\*|\(|\)|\+|\[|\]|\{|\}|\||\.|\?|\\)', token):
        # Does not include the star
        if re.match(r'(\^|\$|\(|\)|\+|\[|\]|\{|\}|\||\.|\?|\\)', token):
            newToken = newToken + u"\\" + token;
            #print token
        else:
            newToken = newToken + token
    
    return newToken;
    

def getPatterns(meta_pattern, version):
           
        cwRegex = u"*";

        localPatterns = {}
        localWords = {}

        
        #Determine the positions of the CWs
        tokens = meta_pattern.split("_");
        W = len(tokens)
        pos = {}
        pos2 = {}
        count = 0;
        for token in tokens:
            if "pw" in token:
                pos[count] = count
            else:
                pos2[count] = count
            count = count + 1

        separator = u"";
        

        f = codecs.open("/Volumes/Transcend/Dropbox/workspace/NLTK/japanese/instances/"+meta_pattern,"r", "utf-8")
        if version == 1:
            out = codecs.open("/Volumes/Transcend/Dropbox/workspace/NLTK/japanese/patterns/v1/"+meta_pattern,"w", "utf-8-sig")   
        else:
            out = codecs.open("/Volumes/Transcend/Dropbox/workspace/NLTK/japanese/patterns/v2/"+meta_pattern,"w", "utf-8-sig")    
            
        for line in f:

            pattern = u"";
            pw_inst = u"";

            tokens = line.split("\t");
            intsCount = int(tokens[2])
            instance = remove_control_characters(tokens[0])
            tokens = list(instance)
            # temp to put all the instances instantiated by the specific pattern.
            temp = {}
            # temp used to put all the patterns than instantiate a specific instance
            temp2 = {}
            print pos
            print pos2
            for index in pos:

                #print "hello"+"".join(tokens[index:index+2])
                pw_inst += u"".join(tokens[index:index+2]) + u" ";
                #[0-2) + [1-3)
                if version == 1:
                    if len(tokens) != (W + 1):
                        continue
                    tokens[index] = cwRegex;
                    tokens[index+1] = cwRegex;
            print instance+ " - "+pw_inst

                
            pw_inst = remove_control_characters(pw_inst.strip());

            temp[pw_inst] = intsCount

            if version == 2:
                # Convert to pattern by first making all a * then getting back the HW
                allStars = cwRegex*len(tokens)
                tokens2 = list(allStars)
                #v2
                # ATTENTION: This is to deal with shorter instances due to whitespace. Please 
                # Find a way to deal with whitespace properly
                if len(tokens) != (W + 1) or len(tokens2) != (W + 1):
                    continue

                for index in pos2:
                    tokens2[index] = tokens[index];
                    tokens2[index+1] = tokens[index+1];
                for token in tokens2:
                    pattern = pattern + separator + token;

            else:
            
                for token in tokens:
                    pattern = pattern + separator + token;

            pattern = remove_control_characters(pattern.strip());
            
            # Add patterns to the list
            if pattern not in localPatterns:
                localPatterns[pattern] = intsCount
            else:
                localPatterns[pattern] = localPatterns[pattern] + intsCount
                temp = localWords[pattern]

                temp[pw_inst] = intsCount

                
            localWords[pattern] = temp


        sorted_patterns = sorted(localPatterns.items(), key=operator.itemgetter(1), reverse=True)

        for (pattern, value) in sorted_patterns:

            temp = localWords[pattern]
            line = pattern + u"\t" + str(len(temp)) + u"\t";

            line = line + str(value) + u"\t";
            
            sorted_instances = sorted(temp.items(), key=operator.itemgetter(1), reverse=True)
            for (instance, value) in sorted_instances:

                line = line + instance + u" " + str(value) + u"\t"
                
            
            out.write(line+u"\n");
       

def selectFinalPatterns(metasPaths, outPath,  minFreq):
        pattern = u"";
        cwRegex = u"."
        patts = {};
        allFiles = []

        for path in metasPaths:
            onlyfiles = [ join(path,f) for f in listdir(path) if isfile(join(path,f)) ]
            allFiles.extend(onlyfiles)

        for f in allFiles:
            #f = join(metasPath,f)
            if "DS_Store" in f or "._" in f:
                continue
            print "Processing "+f
            f = codecs.open(f,"r",encoding='utf-8')
            for line in f:
                        
                tokens = line.split("\t");
                patt = tokens[0].strip();

                if int(tokens[2]) >= minFreq:
                    pattern = u""   
                    tokens = list(regexReservedWords(patt));
                            
                    for token in tokens:
                        if u"*" in token:
                            token = cwRegex;
                                

                        pattern = pattern + token
                        

                    patts[pattern] = patt

        print "Number of patterns: " + str(len(patts))
        out = codecs.open(outPath,"w", "utf-8-sig")
        for pattern in patts:
            out.write(remove_control_characters(pattern)+u"\n")
        out.close()
        

                         
def countPatternsPerEmotion(pattsPath,emoPath,emotion,minFreq):
    print "Processing "+emoPath

    max = 0;
    patts = load(pattsPath)

    pattern = u"";

    cwRegex = u".";

    '''with codecs.open(emoPath,"r",encoding='utf-8') as content_file:
        content = content_file.read()
    jsonContent = json.loads(content)'''

    content_file = codecs.open(emoPath,"r",encoding='utf-8')
    countByEmotion = {}
            
    #for line in jsonContent:
    for line in content_file:
        line = remove_control_characters(line.strip());
        count = 0;
        #print line
        for pattern in patts:
            pattern = pattern.strip()
            #print "Pattern "+pattern
            '''pattern = pattern.strip()
            tokens = list(pattern)
            pattern = ""
            for token in tokens:
                pattern = pattern + token'''
            #result = re.findall(pattern, line,re.UNICODE)
            prog = re.compile(pattern)
            result = prog.finditer(line)
            #result = re.finditer(pattern, line, re.UNICODE)
            for match in result:
                #print pattern+" "+match.group(0)    
                count = count + 1
                #pattern = pattern.replace(cwRegex, "*");
            if pattern in countByEmotion:
                countByEmotion[pattern] = countByEmotion[pattern] + count
            else:
                countByEmotion[pattern] =  count
            count = 0;

    out = codecs.open("/Volumes/Transcend/Dropbox/workspace/NLTK/japanese/patterns/counts/"+str(minFreq)+"/"+ emotion,"w", "utf-8-sig")
    for patt in countByEmotion:
        if countByEmotion[patt] > max:
            max = countByEmotion[patt]
                        
        line = patt + u"\t" + str(countByEmotion[patt])
        out.write(line+u"\n")
            
    out.close()
    print "Max frequency "+str(max)


def countPatternsPerEmotions(pattsPath, emosPath,minFreq):
        
    onlyfiles = [ f for f in listdir(emosPath) if isfile(join(emosPath,f)) ]
    for f in onlyfiles:
        if "DS_Store" in f or "._" in f:
            continue
        emotion = f
        f = join(emosPath,f)
        
        if __name__ == '__main__':
            p = Process(target=countPatternsPerEmotion, args=(pattsPath,f,emotion,minFreq,))
            p.start()
            #p.join()
            
'''          

getInstances("pw_pw_hw");
getInstances("pw_hw_pw");
getInstances("hw_pw_pw");

getInstances("hw_hw_pw");
getInstances("hw_pw_hw");
getInstances("pw_hw_hw");

getInstances("pw_hw");
getInstances("hw_pw");

'''

'''getPatterns("pw_pw_hw",1);
getPatterns("pw_hw_pw",1);
getPatterns("hw_pw_pw",1);

getPatterns("hw_hw_pw",1);
getPatterns("hw_pw_hw",1);
getPatterns("pw_hw_hw",1);

getPatterns("pw_hw",1);
getPatterns("hw_pw",1);


getPatterns("pw_pw_hw",2);
getPatterns("pw_hw_pw",2);
getPatterns("hw_pw_pw",2);

getPatterns("hw_hw_pw",2);
getPatterns("hw_pw_hw",2);
getPatterns("pw_hw_hw",2);

getPatterns("pw_hw",2);
getPatterns("hw_pw",2);

'''

#metasPaths = ["/Volumes/Transcend/Dropbox/workspace/NLTK/japanese/patterns/v1","/Volumes/Transcend/Dropbox/workspace/NLTK/japanese/patterns/v2"]
minFreq = 30
#selectFinalPatterns(metasPaths, "/Volumes/Transcend/Dropbox/workspace/NLTK/japanese/patterns/patterns_"+str(minFreq),  minFreq)

#countPatternsPerEmotions("patterns/patterns_"+str(minFreq), "Murmur/total/moods",minFreq)'''
countPatternsPerEmotions("/Volumes/Transcend/Dropbox/workspace/NLTK/japanese/patterns/patterns_"+str(minFreq),"/Volumes/Transcend/Dropbox/workspace/NLTK/japanese/data_original/training",30)
#countPatternsPerEmotions("patterns/patterns_0", "Murmur/cleansing/moods")
