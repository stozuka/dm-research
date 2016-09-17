import codecs
import unicodedata
import re
from os import listdir
from os.path import isfile, join, basename
import numpy as np
import sys
from multiprocessing import Process

reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

def remove_control_characters(s):
    return u"".join(ch for ch in s if unicodedata.category(ch)[0]!="C")

def loadModels(path):
    print "Loading Models"
    models = {}
    onlyFiles = [ f for f in listdir(path) if isfile(join(path,f)) ]   

    for f in onlyFiles:
        
        if "DS_Store" in f:
            continue
        print "Processing "+f
        emotion = f.split(".")[0]
        f = join(path,f)
        f = codecs.open(f,"r",encoding='utf-8') 

        patts = {}
               
        pos = 0 
        for line in f:
            
            #print line
            tokens = line.split("\t")
                        
            pattern = remove_control_characters(tokens[0].strip())
                     
            pos = pos + 1
            patts[pattern] =  pos

                     
        models[emotion] = patts

    return models;

def loadMatrix(path):
    #print "Loading matrix "+path

    f = codecs.open(path,"r",encoding='utf-8')

    emotions = {}
    patterns = {}

    matrix = []

    inEmotions = 0
    inPatterns = 0
    inMatrix = 0

    for line in f:
        line = line.strip()

        if "Emotions" in line:
            inEmotions = 1
            continue

        if "Patterns" in line:
            inPatterns = 1
            inEmotions = 0
            continue

        if "Matrix" in line:
            inMatrix = 1
            inPatterns = 0
            inEmotions = 0
            continue

        if inEmotions and len(line) > 0:
            #print "Emotion "+line
            tokens = line.split("\t");
            emotions[int(tokens[0])] = remove_control_characters(tokens[1].strip())
        
        if inPatterns and len(line) > 0:  
            tokens = line.strip().split("\t")
            patt = remove_control_characters(tokens[1].strip())
            patterns[int(tokens[0])] =  patt

            '''if len(patt) < 2:
                print "Small pattern "+patt'''
        
        if inMatrix and len(line) > 0: 
            row = [];
            tokens = line.split(" ");
            
            for val in tokens:
                row.append(float(val))
    
            matrix.append(row)
    
    #print "Done loading %d Emotions %d Patterns and %d Rows"%(len(emotions),len(patterns),len(matrix))
    #print emotions
    #print patterns
    #print np.array(matrix) 
    return emotions, patterns, np.array(matrix)     

    

def evalWithMultiple(post, emotion,emotionModel):
    post = remove_control_characters(post)
    finalScore = 0.0
    for patt in emotionModel:
        prog = re.compile(patt)
        result = prog.finditer(post)
        #result = re.finditer(pattern, line, re.UNICODE)
        for match in result:
            #print patt+" "+match.group(0)+" "+str(emotionModel[patt]  )  
            finalScore = finalScore + emotionModel[patt];
    print emotion+"\t"+str(finalScore)
    
    return finalScore  


def evalWithMatrix(post,emotions,patterns,matrix, correct_emotion, mode ,out, out2):
    # Mode 1 - single guess, Mode 2 - Double guess
    #print "Evaluatinf post "+post
    post = remove_control_characters(post)
    vector = []
    for index in patterns:
        #print index
        patt = patterns[index]
        count = 0;
        if len(remove_control_characters(patt)) > 1:
            prog = re.compile(remove_control_characters(patt))
            result = prog.finditer(post)
            
            for match in result:
                count = count + 1
                #print "Found "+patt+" "+match.group(0)+" "+str(index)
    
        
        vector.append(count)
    vector = np.transpose(np.array(vector))
    #print vector
    
    result = np.dot(matrix,vector)

    order = np.argsort(result)

    '''for i in order:
        emotion = emotions[i]
        score = result[i]
        print emotion + "\t" +str(score)'''

    emotion = emotions[order[0]]
    emotion2 = emotions[order[1]]
    #print "Detected %s correct %s"%(emotion,correct_emotion)
    out.write(post+"\t"+emotion+"\t"+emotion2+"\n")
    out2.write(post+"\t"+emotion+"\t"+emotion2+"\n")
    if mode == 1:
        if emotion in correct_emotion:
            return 1
    else:
        if emotion in correct_emotion or emotion2 in correct_emotion:
            return 1
    
    return 0

def classifyUsingMultiple(modelsPath, postsPath):
    

    models = loadModels(modelsPath)

    f = codecs.open(postsPath,"r",encoding='utf-8') 
    for post in f:
        for emotion in models:
            if __name__ == '__main__':
                p = Process(target=evalWithMultiple, args=(post,emotion,models[emotion],))
                p.start()

    
def classifyUsingMatrix(matrixPath, postsPath, out):
   
    
    [emotions,patterns,matrix] = loadMatrix(matrixPath)

    correct_emotion = basename(postsPath)

    out2 = codecs.open("/Volumes/Transcend/Dropbox/workspace/NLTK/japanese/output/classification_%s"%correct_emotion,"w", "utf-8-sig")

    count_eval = 0
    count_correct = 0
    
    f = codecs.open(postsPath,"r",encoding='utf-8') 
    for post in f:
        post = post.split("\t")[0]
        val = evalWithMatrix(post,emotions,patterns,matrix,correct_emotion,1, out,out2)
        count_eval = count_eval + 1
        count_correct = count_correct + val
        #print "Eval %d - correct %d - Acc %f"%(count_eval,count_correct,float(count_correct)/float(count_eval))

    out2.close
    
    print "Eval %d - correct %d - Acc %f"%(count_eval,count_correct,float(count_correct)/float(count_eval))
    return count_eval,count_correct

def eval(matrix,root):
    big_eval = 0
    big_correct = 0
    data_files = [
    join(root, d) for d in listdir(root) if "._" not in d]

    out = codecs.open("/Volumes/Transcend/Dropbox/workspace/NLTK/japanese/output/classification","w", "utf-8-sig")

    for file in data_files:
        print file
        
        count_eval,count_correct = classifyUsingMatrix(matrix,file,out)

        big_eval = big_eval + count_eval
        big_correct = big_correct + count_correct

    print "Total eval %d - correct %d - Acc %f"%(big_eval,big_correct,float(big_correct)/float(big_eval))

    '''for folder in data_folders:
        images = [os.path.join(folder, name) for name in os.listdir(folder) if os.path.isfile(os.path.join(folder, name))]

    '''

    out.close()

minFreq = 30
#classifyUsingMultiple("models/multiple/"+str(minFreq), "data/test")
#classifyUsingMatrix("/Volumes/Transcend/Dropbox/workspace/NLTK/japanese/models/matrix/matrix_"+str(minFreq), "/Volumes/Transcend/Dropbox/workspace/NLTK/japanese/data_original/testing/surprise")

eval("/Volumes/Transcend/Dropbox/workspace/NLTK/japanese/models/matrix/matrix_"+str(minFreq), "/Volumes/Transcend/Dropbox/workspace/NLTK/japanese/data_original/testing/")


