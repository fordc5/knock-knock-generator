##
# @author: CF, GM
# @date: May 2019
#
# idea is to take tokens and find occurence in dataset of sentences. Select 
# the sentence following the occurence.

from collections import defaultdict

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

tokens = [line.strip().split(" ")[0] for line in open("./tokenizing_scripts/tokens/init_results_2d", "r")]

# iterate over tokens and if token appears as key
# then pick sentence
for token in tokens:
    if token in word_dict:
        response = word_dict[token][0]
        print(token, response)

