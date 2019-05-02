##
# @author: CF, GM
# @date: May 2019
#
# Mostly data cleaning generate file of dialogues with 
# breaks in dialogue seperated by '$$'


movie_lines = {}
for line in open("./data/movie_lines.txt", "r", errors="replace"):
    #line = unicode(line, errors='replace')
    line_split = line.split("+++$+++")
    movie_lines[line_split[0].strip()] = line_split[-1].strip()

movie_conversations = [line.strip().split("+++$+++")[-1].strip() for line in open("./data/movie_conversations.txt", "r")]

# generate lines
lines = []
for conversation in movie_conversations:
    conversation = conversation[1:-1].split(",")
    dialogue = []
    for line in conversation:
        line = line.strip().strip("\'")
        if line in movie_lines:
            dialogue.append(movie_lines[line])
    lines.append(dialogue)



# write to file
f = open("./response_generation/movie_scripts/dialogues.txt", "a")
for line in lines:
    strg = "$$".join(line) + "\n"
    f.write(strg)
f.close()
