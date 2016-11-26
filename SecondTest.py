from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
import json
import nltk
from nltk.corpus import stopwords

def get_continuous_chunks(text):
    chunked = ne_chunk(pos_tag(word_tokenize(text)))
    #chunked = ne_chunk(text, binary=True)

    prev = None
    continuous_chunk = []
    current_chunk = []
    for i in chunked:
            if type(i) == Tree:
                    current_chunk.append(" ".join([token for token, pos in i.leaves()]))
            elif current_chunk:
                    named_entity = " ".join(current_chunk)
                    if named_entity not in continuous_chunk:
                            continuous_chunk.append(named_entity)
                            current_chunk = []
            else:
                    continue
    return continuous_chunk

# sdfkljsdf
stop_words = set(stopwords.words('english'))

# Data
with open('data.json') as json_data:
        data = json.load(json_data)
title = data[0]['title']
words = nltk.word_tokenize(title)
filtered_sentence = []
for w in words:
    if w not in stop_words:
        filtered_sentence.append(w)
tagged = nltk.pos_tag(filtered_sentence)
print(tagged)
print(get_continuous_chunks(tagged))
