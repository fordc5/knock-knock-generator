import pronouncing
phones_ = pronouncing.phones_for_word("")
if len(phones_) > 0:
    phones = phones_[0]
    #print(pronouncing.search(phones+"$")[:10])
else:
    print("no phones found.")


# print(pronouncing.phones_for_word("who"))
# print(pronouncing.phones_for_word("ew"))
# print(pronouncing.phones_for_word("oo"))
# print(pronouncing.phones_for_word("ooh"))
# print(pronouncing.phones_for_word("hoo"))

word_candidates = pronouncing.search("(UW1|UW2)$")

for word in word_candidates:
    phone = pronouncing.phones_for_word(word)[0]

    phone_split = phone.split()

    phone_split.pop()

    phone = " ".join(phone_split)

    results = pronouncing.search(phone)

    for result in results:
        if result != word and result in word:
            print(word, result)

    # if result != word:
    #     print(True)
    #     print(word, result)

    


#phone = pronouncing.phones_for_word("cashew")
#print(phone)