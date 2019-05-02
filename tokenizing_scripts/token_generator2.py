##
# Token Generator
# @authors: CF, GM
# @date: 5/2019

import pronouncing

# replace with path to data
# one word per line
words = [line.strip() for line in open("./data/words_alpha.txt", "r")]

# replace with path to data
# one word per line
# format of clex_lexicon is: adj_itr(ablaze, ablaze).
word_verification = [line.strip().split("(")[1].split(",")[0] for line in open("./data/clex_lexicon.pl", "r")]

# literal phonetic endings
phones = ["who", "ew", "ewe", "ooo", "ooh", "oo", "hue", "ue", "eau", "eww", "hu"]

for word in words:
    word = word.strip()
    for phone in phones:
        if word.endswith(phone):
            base = word[:-len(phone)].strip() # get base/token of word
            if base in words and base in word_verification and len(base) > 1: # if not trivial word
                if len(pronouncing.phones_for_word(word)) > 0: # if pronounciation exists
                    if any(x in pronouncing.phones_for_word(word)[0].split() for x in ["UW0", "UW1", "UW2"]): # if ends in 'ew' sound
                        print(word, base)
