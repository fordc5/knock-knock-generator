import os
import re
import time
import pickle
import linecache
import random
from multiprocessing import Process


def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())


wikipedia_sentences = os.getcwd()+ "/data/wikisample.txt"

def tokenize(sent):
    sent = sent.lower()
    pattern_period = re.compile(r'([\.!?]\n)$',re.I)
    pattern_comma = re.compile(r'([,\"\)\(:\'])',re.I)
    sent = pattern_period.sub(r" \1",sent)
    sent = pattern_comma.sub(r" \1 ",sent)
    token_list = ["<START>"] + sent.split(" ") + ["<END>"]
    return token_list

def n_gram(w_vec, n):
    res = []
    for i in range(0,len(w_vec)-n+1):
        n_gram = w_vec[i:i+n]
        res.append(n_gram)
    return res

def randomize_file(filename):
    f = open(filename,"r")
    lines = f.readlines();
    f.close()
    f = open(filename+".randomized","w+")
    n = len(lines)
    while(n>0):
        print(n)
        i = random.randint(0,len(lines))
        f.write(lines[i])
        del lines[i]
        n = len(lines)
    f.close()
    return filename+".randomized"

def pick_from_probability_distribution(d):
    if d==None:
        print("hh")
        return None
    elif len(d.keys())==1:
        return list(d.keys())[0]
    options = list(d.keys())
    frequencies = list(d.values())
    sum = 0
    aux = []
    for frq in frequencies:
        sum = sum + frq
        aux.append(sum)
    r = random.randint(1,sum)
    for i in range(1,len(aux)):
        if (aux[i-1]<r) and (aux[i]>=r):
            return options[i]



class SentenceGenerator:

    def __init__(self, file_training_loc):
        file = open(file_training_loc,"r")
        file.seek(0,2) #Jumps to the end
        endLoc = file.tell()    #Give you the end location (characters from start)
        file.seek(0)   #Jump to the beginning of the file again
        i = 0
        sent = file.readline()
        last_check = 0.0
        prev = 0
        self.u_dict = {}
        self.b_dict = {}
        self.t_dict = {}
        self.word_to_int = {}
        self.int_to_word = {}
        self.word_count = 0
        start = time.time()
        while(endLoc != file.tell()):
            self.process_sentence(sent)
            sent = file.readline()
            i = i + 1
            current = time.time() - start
            if (int(current)+1)%10==0 and last_check!=int(current)+1:
                last_check = int(current)+1
        print(current,": ",(i - prev)/current," sentences/second")
        file.close()


    def tuple_to_bigram(self,t):
        a = self.word_to_int[t[0]]
        b = self.word_to_int[t[1]]
        return (a,b)

    def generate_next(self,root):
        i = self.word_to_int[root]
        d = self.b_dict.get(i)
        return self.int_to_word.get(pick_from_probability_distribution(d))



    def process_sentence(self,sent):
        sent_vec = tokenize(sent)
        for word in sent_vec:
            if word not in self.word_to_int.keys():
                self.word_to_int[word] = self.word_count
                self.int_to_word[self.word_count] = word
                self.word_count = self.word_count + 1
            self.u_dict[self.word_to_int[word]] = self.u_dict.get(self.word_to_int[word],0)+1
        if len(sent_vec)>2:
            trigrams = n_gram(sent_vec,3)
            b_1 = self.word_to_int[trigrams[0][0]]
            b_2 = self.word_to_int[trigrams[0][1]]
            sd = self.b_dict.get(b_1,{})
            sd[b_2] = sd.get(b_2,0)+1
            self.b_dict[b_1] = sd
            for gram in trigrams:
                #key = (self.word_to_int[gram[0]],self.word_to_int[gram[1]])
                #v = self.word_to_int[gram[2]]
                #sd = self.t_dict.get(key,{})
                #sd[v] = sd.get(v,0)+1
                #self.t_dict[key] = sd

                b_1 = self.word_to_int[gram[1]]
                b_2 = self.word_to_int[gram[2]]
                sd = self.b_dict.get(b_1,{})
                sd[b_2] = sd.get(b_2,0)+1
                self.b_dict[b_1] = sd
        elif len(sent_vec)==2:
            b_1 = self.word_to_int[sent_vec[0]]
            b_2 = self.word_to_int[sent_vec[1]]
            sd = self.b_dict.get(b_1,{})
            sd[b_2] = sd.get(b_2,0)+1
            self.b_dict[b_1] = sd


    def generate_sentence_starting_with(self,root):
        l= []
        next = self.generate_next(root)
        while(next!="<END>" and next!=None):
            print(next)
            l.append(next)
            next = self.generate_next(next)
        return l


if __name__ == '__main__':
    s = SentenceGenerator(wikipedia_sentences)
    r = list(s.u_dict.keys())
    print(s.generate_sentence_starting_with("cashew"))
