##
#
# @date: 5/2019

sentences = [line.strip() for line in open("./data/sentences.txt", "r")]

tokens = [line.strip().split(" ")[0] for line in open("./tokenizing_scripts/tokens/init_results_2d", "r")]

#psuedocode
for token in tokens:
    for paragraph in paragraphs:
        if word in paragraph:
            return sentence after sentence with first occurence.

