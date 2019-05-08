##
# @author: CF, GM
# @date: May 2019
#
# idea is to take tokens and find occurence in dataset of sentences. Select 
# the sentence following the occurence.

from collections import defaultdict
import random

sentences = [line.strip() for line in open("./response_generation/movie_scripts/dialogues.txt", "r")]

# dialogue preprocessing
# need O(1) look up for dialogues with keyword
# use dict with keys as words and values as list of sentences that follow
word_dict = defaultdict(list)
for dialogue in sentences:
    sentence_split = dialogue.split("$$")
    for idx, sentence in enumerate(sentence_split):
        if idx < len(sentence_split) - 1:
            for word in sentence.split(" "):
                word_dict[word].append(sentence_split[idx+1])

tokens = []
for line in open("./tokenizing_scripts/tokens/init_results_cross", "r"):
    line = line.strip()
    if len(line) > 1 and line[0] != "/":
        tokens.append((line.split(" ")[0], (line.split(" ")[1])))

# iterate over tokens and if token appears as key
# then pick sentence
for token in tokens:
    (word, tok) = token
    if word in word_dict:
        rand_index = random.randint(0, len(word_dict[word])-1)
        response = word_dict[word][rand_index]
        print()
        print(tok, word, word_dict[word])
        # print("Knock knock.")
        # print("Who's there?")
        # print(tok)
        # print(tok + ' who?')
        # print(response)
        # print(' ')


