##
# Token Generator
# @authors: CF, GM
# @date: 4/2019

import pronouncing

# replace with path to data
# one word per line
lines = [line.strip() for line in open("./data/words_alpha.txt", "r")]

phones = ["who", "ew", "ewe", "ooo", "ooh", "oo", "hue", "ue", "eau", "eww", "hu"]

for line in lines:
    line = line.strip()
    for phone in phones:
        if line.endswith(phone):
            base = line[:-len(phone)].strip() # get base/token of word
            if base in lines and len(base)>1: # if not trivial 'word'
                if len(pronouncing.phones_for_word(line)) > 0: # if pronounciation exists
                    if any(x in pronouncing.phones_for_word(line)[0].split() for x in ["UW0", "UW1", "UW2"]): # if ends in 'ew' sound
                        print(line, base)
