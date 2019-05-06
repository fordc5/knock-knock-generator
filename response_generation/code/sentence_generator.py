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


wikipedia_sentences = os.getcwd()+ "/data/wikisent2.txt.randomized"

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
        print("00")
        return ""
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
    return options[-1]

def read_ngrams(file):
    d = {}
    with open(file,"r") as f:
        for line in f:
            ar = line.split()
            freq = int(ar[0])
            key = " ".join(ar[1:-1])
            val = ar[-1]
            if key not in d:
                d[key] = {}
            d[key][val] = freq
    return d


class SentenceGenerator:

    def __init__(self, file_training_loc):
        self.five_gram_dict = read_ngrams(file_training_loc+"w5_.txt")
        self.four_gram_dict = read_ngrams(file_training_loc+"w4_.txt")
        self.bi_gram_dict = read_ngrams(file_training_loc+"w2_.txt")
        self.tri_gram_dict = read_ngrams(file_training_loc+"w3_.txt")

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
        gr = [self.bi_gram_dict,self.tri_gram_dict,self.four_gram_dict]
        l = [root]
        while True:
            d = gr[len(l)-1].get(root,{})
            if d == {}:
                return l
            else:
                x = pick_from_probability_distribution(d)
                l = l + [x]
                root = " ".join(l)
                if len(l)>len(gr):
                    break
        #return l
        for i in range(5):
            x = self.five_gram_dict.get(" ".join(l[-5:]),{})
            if x == {}:
                return l
            else:
                c = pick_from_probability_distribution(x)
                l = l + [c]
        return l


    def get_tokens(self,file):
        l = []
        with open(file,"r") as f:
            for line in f:
                if len(re.findall(r"^\//",line))<1 and len(line.split(" "))>1:
                    l.append(line.split(" ")[0])
                    t = self.generate_sentence_starting_with(line.split(" ")[0])
                    if len(t)>2:
                        base = line.split(" ")[1].split("\n")[0]
                        resp = " ".join(t)
                        joke = "Knock knock.\nWho's there?\n"+base+".\n"+base+" who?\n"+resp
                        print(joke)
                        print("---------------------------")




if __name__ == '__main__':
    five_grams = os.getcwd()+ "/response_generation/data/ngrams/"
    s = SentenceGenerator(five_grams)

    tokens = os.getcwd()+ "/tokenizing_scripts/tokens/init_results_cross"
    for ext in os.listdir(os.getcwd()+ "/tokenizing_scripts/tokens/"):
        token = os.getcwd()+ "/tokenizing_scripts/tokens/"+ext
        s.get_tokens(token)
    """
    r = list(s.u_dict.keys())
    print(s.generate_sentence_starting_with("cashew"))
    """
