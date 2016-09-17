import math
import codecs
from os import listdir
from os.path import isfile, join
import re
import unicodedata
import operator
import sys

reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

def load( path):
    words = {}
    f = codecs.open(path,"r", "utf-8")
    for word in f:
        word = remove_control_characters(word)
        if len(word.strip()) > 0:
            words[word.strip()] = word.strip()
    print "Loaded %s Patterns"%str(len(words))
    return words

def remove_control_characters(s):
    return u"".join(ch for ch in s if unicodedata.category(ch)[0]!="C")

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
    
    return remove_control_characters(newToken);

# Pattern Frequency
def pf(path):
    print "Processing PF"
    pf = {}
    onlyFiles = [ f for f in listdir(path) if isfile(join(path,f)) ]   

    max = 0.0;

    for f in onlyFiles:
        print "Processing "+f
        if "DS_Store" in f or "._" in f:
            continue
        emotion = f.split(".")[0]
        f = join(path,f)
        f = codecs.open(f,"r",encoding='utf-8') 

        patts = {}
                
        for line in f:
            
            #print line
            tokens = line.split("\t")
            if float(tokens[1]) > max:
                max = float(tokens[1])
                        
            pattern = remove_control_characters(tokens[0].strip())
         
            if pattern in patts:
                print "Repeated PF "+pattern 
                        
            value = math.log10(float(tokens[1]) + 1)
            patts[pattern] =  value

            '''if value > 0.0:
                print pattern + " "  + str(value)'''
                     
        if emotion in pf:
            oldPatts = pf[emotion]
            patts.update(oldPatts);
                 
        pf[emotion] = patts

               

    print "Max PF " + str(max)

    return pf;

# Inverse Emotion Frequency
def ief(pf):
    print "Processing IEF"
    print len(pf)
    ief = {}
    for emotion in pf:
            
        pfEmo = pf[emotion]
        for patt in pfEmo:
            
            exists = 0.0;
            if pfEmo[patt] > 0.0:
                exists = 1.0;
                
            if patt in ief:
                ief[patt] = ief.get(patt) + exists
            else:
                ief[patt] = exists
    count = 0   
    count2 = 0     
    for patt in ief:
        
        if ief[patt] != 0:
            val = float(len(pf)) / float(ief[patt])
            #double val = Math.log10(1 + 6.0 / ((double) icf.get(patt) + 1.0));
        else:
            val = 0.0;
            
        if val == 0.0:
            print patt.strip()
            count = count + 1
        else:
            count2 = count2 + 1
        ief[patt] = val
    print "Total not found in any file "+str(count)
    print "Total found some file "+str(count2)
    return ief

def div(metasPaths,minFreq):
    print "Processing DIV"
    scIndex = 1
    cwRegex = u"."
    div = {}

    allFiles = []

    for path in metasPaths:
        onlyfiles = [ join(path,f) for f in listdir(path) if isfile(join(path,f)) ]
        allFiles.extend(onlyfiles)
        
    for f in allFiles:
            #f = join(metasPath,f)
        print "Processing "+f
        if "DS_Store" in f or "._" in f:
            continue
        f = codecs.open(f,"r",encoding='utf-8')

        for line in f:
                       
            tokens = line.split("\t");
            patt = remove_control_characters(tokens[0].strip());
            #print "DIV "+patt
            if int(tokens[2]) >= minFreq:
                ratio = math.log10(float(tokens[scIndex]));
                #ratio = (Double.parseDouble(tokens[2]) / Double.parseDouble(tokens[1]));
                pattern = u""   
                tokens = list(regexReservedWords(patt));
                            
                for token in tokens:
                    if u"*" in token:
                        token = cwRegex;
                                

                    pattern = pattern + token
                    
                div[pattern] = ratio
                print "DIV "+pattern
    
    print "Number of patterns with DIV: " + str(len(div));
        
    return div;

def ed(pf,ief,div):
    print "Computing ED"
    ed = {}
    found = {}
    notFound = {}
    for emotion in pf:
        pfEmo = pf[emotion]
        edEmo = {}
        for patt in pfEmo:
            if patt in div:
                #print "Found " + patt  
                found[patt] = patt       
                edEmo[patt] =  pfEmo[patt] * ief[patt] * div[patt]     
            else:
                notFound[patt] = patt
                
                
           
        ed[emotion] = edEmo
    print "Number of patterns not found: " + str(len(notFound));
    for patt in notFound:
        print patt
    return ed

def saveMultiple(ed,minFreq):
    print "Saving to multiple files"
    for emotion in ed:
        edEmo = ed[emotion]
        out = codecs.open("/Volumes/Transcend/Dropbox/workspace/NLTK/japanese/models/multiple/"+str(minFreq)+"/"+emotion,"w", "utf-8-sig")
        sorted_patterns = sorted(edEmo.items(), key=operator.itemgetter(1), reverse=True)
        for (pattern, value) in sorted_patterns:
            out.write(remove_control_characters(pattern) + u"\t" + unicode(value)+u"\n");
        out.close()


def saveMatrix(ed,minFreq):
    print "Saving Emotion Matrix"

    out = codecs.open("/Volumes/Transcend/Dropbox/workspace/NLTK/japanese/models/matrix/matrix_"+str(minFreq),"w", "utf-8-sig")

    index = 0
    out.write("%%Emotions%%");
    for emotion in ed:
        out.write("\n")
        out.write(unicode(index)+"\t"+emotion)
        index = index + 1
        
    out.write("\n")
    out.write("\n") 
    out.write("%%Patterns%%");
    patts = load("/Volumes/Transcend/Dropbox/workspace/NLTK/japanese/patterns/patterns_"+str(minFreq))

    index = 0
    for pattern in patts :      
        out.write("\n")
        out.write(str(index)+"\t"+pattern);
        #out.write(pattern);
        index = index + 1
            
    out.write("\n")
    out.write("\n")
    out.write("%%Matrix%%");
    out.write("\n")
    
    for emotion in ed:
        #line = emotion+"\t"
        line = ""
        edEmo = ed[emotion]
        rank = {}
        sorted_patterns = sorted(edEmo.items(), key=operator.itemgetter(1), reverse=True)
        pos = 0
        for (pattern, value) in sorted_patterns:
            pos = pos + 1
            rank[pattern] = pos
        index = 0
        for pattern in patts:
            #line = line + str(index)+":"+pattern+":"+unicode(rank[pattern])+u" "
            print pattern
            line = line + unicode(rank[pattern])+u" "
            index = index + 1
        line = line.strip()+u"\n"    
        out.write(line)

    out.close();


minFreq = 30
pf = pf("/Volumes/Transcend/Dropbox/workspace/NLTK/japanese/patterns/counts/"+str(minFreq))
ief = ief(pf)
metasPaths = ["/Volumes/Transcend/Dropbox/workspace/NLTK/japanese/patterns/v1","/Volumes/Transcend/Dropbox/workspace/NLTK/japanese/patterns/v2"]
div = div(metasPaths,minFreq)
ed = ed(pf,ief,div)
saveMultiple(ed,minFreq)
saveMatrix(ed,minFreq)