# knock-knock-generator

NLP Final Project <br />
“Jokes on you”

### Members: <br />
Connor Ford and Gabe Magee

### Summary:
- We are currently generating a single class of knock-knock joke: <br />
(a) knock knock <br />
(b) who's there? <br />
(a) _token_ <br />
(b) _token_ who? <br />
(a) Response related to _token_ + 'ew'/'who' sounding word. <br />
- We first iterate over a list of English words searching for those that end in an 'ew'/'who' sound. 
- Then we take the base (token) of the word minus the 'ew'/'who' sound.
- The token must be a word so we search for it in the english word corpus.
- We finally generate a bi-gram based response from the word and its surrounding context in another english-language corpus.

### Results: 
Joke #1:

Knock Knock.

Who's There?

Cash

Cash who?

Cashew apple ii cd of the target for championship at 124.

(As you can see, this doesn't make much sense)

### Problems: 
- We are currently generating a small sample size of jokes. We have about 15 tokens for our joke format and don't forsee adding many more to this count. We might add an additional class of knock-knock jokes to extend this a bit.
- We also plan to generate the responses in a couple other ways. We might experiment with a sentence-after approach; or change the english-language corpus.
- Our bi-gram chaining approach has lots of issues right now. Like it will generate a string of loosely generated words, possibly cyclic. As detailed above we are looking to implement and test some other methods.

### Hours: <br />
Connor - 1hr Fri, 4 hrs Sat, 2 hrs Sun <br />
Gabe - 1hr Fri, 4 hrs Sat, 2 hrs Sun



## Data 
(English words) https://github.com/dwyl/english-words <br />
(Phonetic compositions) https://github.com/aparrish/pronouncingpy <br />
(Wikipedia English Sentences)https://www.kaggle.com/mikeortman/wikipedia-sentences<br />
(Second/shorter list of English words) http://attempto.ifi.uzh.ch/site/description/ <br />
(Movie scripts) https://www.cs.cornell.edu/~cristian/Cornell_Movie-Dialogs_Corpus.html


