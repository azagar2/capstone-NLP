import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import PunktSentenceTokenizer
from nltk.tree import Tree
import json
import itertools
import re
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from functools import lru_cache
from pprint import pprint

# STOP WORDS
stop_words = set(stopwords.words('english'))
wnl = WordNetLemmatizer()

# Big arrays
event_titles = []
event_title_tags = []
event_categories = []
lord_set = []
event_description_tags = []

bad_words = ['ticket', 'tickets', 'event', 'events', 'time', 'door', 'entrance']

def main():

    mega_corpus = []

    # IMPORT DATA FROM JSON FILE
    with open('../scraper/user.json') as json_data:
        data = json.load(json_data)

    # Master arrays
    allSets = []

    # Go through all data (titles for now)
    for event in data[:]:

        # Title
        title = event['title']
        event_titles.append(title)
        title = re.sub('[^a-zA-Z0-9 ]', " ", title)

        # Category
        category = event['category_key']
        event_categories.append(category)

        # Description
        example_sentence = event['description'].lower()
        example_sentence = re.sub('[^a-zA-Z ]', " ", example_sentence)

        ################################################################

        # Process title
        title_tags = list(set(title_chunking(title) + title_chunking(title.lower())))
        event_title_tags.append(title_tags)
        #print("TITLE TAGS:   " + str(title_tags))

        # Use Punkt Tokenizer - CONTENT
        custom_sent_tokenizer = PunktSentenceTokenizer() #example_sentence
        tokenized = custom_sent_tokenizer.tokenize(example_sentence)
        description_tags = process_content(tokenized)
        allSets.append(description_tags)
        combo = list(set(title_tags + description_tags))
        lord_set.append(combo)
        mega_corpus += combo

    mega_corpus = set(mega_corpus);
    #print(mega_corpus)

    with open('../scraper/new-events.json') as json_data:
        data = json.load(json_data)

    eventList = [];
    for event in data[:]:
        # Title
        title = event['title']
        event_titles.append(title)
        title = re.sub('[^a-zA-Z0-9 ]', " ", title)

        # Description
        example_sentence = event['description'].lower()
        example_sentence = re.sub('[^a-zA-Z ]', " ", example_sentence);

        # Process title
        title_tags = list(set(title_chunking(title) + title_chunking(title.lower())))
        event_title_tags.append(title_tags)

        custom_sent_tokenizer = PunktSentenceTokenizer() #example_sentence
        tokenized = custom_sent_tokenizer.tokenize(example_sentence)
        description_tags = process_content(tokenized)
        combo = list(set(title_tags + description_tags))
        intersection = list(mega_corpus.intersection(combo));
        ratio = len(intersection)/len(combo);
        data = {}
        data['title'] = event['title']
        data['ratio'] = ratio
        data['category'] = event['category'];
        eventList.append(data);
    pprint(list(sorted(eventList, key=sortFn)));
def sortFn(s):
    return s['ratio'];

#################################

def process_title(title):
    words = nltk.word_tokenize(title)
    filtered_sentence = []
    nonfiltered_sentence = []
    for w in words:
        nonfiltered_sentence.append(w)
        if w not in stop_words:
            filtered_sentence.append(w)
    tagged = nltk.pos_tag(filtered_sentence)
    tagged2 = nltk.pos_tag(filtered_sentence)
    print(tagged)
    print(tagged2)
    namedEntTrue = nltk.ne_chunk(tagged, binary=True)
    namedEntFalse = nltk.ne_chunk(tagged, binary=False)
    #namedEntTrue.draw()
    named_entities = []
    named_entities_false = []
    master_titles = []


    #for subtree in namedEntTrue.subtrees(filter=lambda t: (t.label() == 'NE')):
    for subtree in namedEntTrue.subtrees():
        if subtree.label() == 'NE':
            for s in list(subtree):
                named_entities.append(s)

    for subtree in namedEntFalse.subtrees():
        if subtree.label() != 'S':
            named_entities_false.append(list(subtree))

    # Matching from both lists
    for group in named_entities_false:
        if len(group) == 0:
            continue
        elif len(group) == 1:
            g = group[0]
            if g in named_entities:
                named_entities.remove(g)
            master_titles.append(g[0])
        else:
            temp = []
            for g in group:
                temp.append(g[0])
                if g in named_entities:
                    named_entities.remove(g)
            #print("*************** " + " ".join(temp))
            master_titles.append(" ".join(temp))

    if len(named_entities) > 0:
        for item in named_entities:
            master_titles.append(item[0])


    # print(named_entities)

    if len(master_titles) > 0:
        return(master_titles)


def title_chunking(title):

        words = nltk.word_tokenize(title)
        filtered_sentence = []
        for w in words:
            #if (w not in stop_words) and (len(w) > 2):
            if (len(w) > 2):
                filtered_sentence.append(w)
        tagged = nltk.pos_tag(filtered_sentence) #words
        chunkParser = nltk.RegexpParser(r"""Chunk: {<J.+>+<N.+>?}""")
        chunkParser2 = nltk.RegexpParser(r"""Chunk: {<JJ>*<NN>}""")
        chunkParser3 = nltk.RegexpParser(r"""Chunk: {<NN.*>+}""")
        chunked = chunkParser.parse(tagged)
        chunked2 = chunkParser2.parse(tagged)
        chunked3 = chunkParser3.parse(tagged)

        # Parse subtrees
        chunkedList = parseSubtree(chunked.subtrees(filter=lambda t: t.label() == 'Chunk'), False)
        chunked2List = parseSubtree(chunked2.subtrees(filter=lambda t: t.label() == 'Chunk'), False)
        chunked3List = parseSubtree(chunked3.subtrees(filter=lambda t: t.label() == 'Chunk'), False)

        # Generate set of tags from all lists
        uniqueTags = list(set(chunkedList + chunked2List + chunked3List))
        return uniqueTags


def process_content(tokenized):
        for i in tokenized[:]: #tokenized[:3]
            words = nltk.word_tokenize(i)
            #filtered_sentence = [w for w in words if not w in stop_words]
            filtered_sentence = []
            for w in words:
                #if (w not in stop_words) and (len(w) > 2):
                if (len(w) > 2):
                    filtered_sentence.append(w)

            tagged = nltk.pos_tag(filtered_sentence) #words
            chunkParser = nltk.RegexpParser(r"""Chunk: {<J.+>+<N.+>?}""")
            chunkParser2 = nltk.RegexpParser(r"""Chunk: {<JJ>*<NN>}""")
            chunkParser3 = nltk.RegexpParser(r"""Chunk: {<NN.*>+}""")
            chunked = chunkParser.parse(tagged)
            chunked2 = chunkParser2.parse(tagged)
            chunked3 = chunkParser3.parse(tagged)

            chunkedList = parseSubtree(chunked.subtrees(filter=lambda t: t.label() == 'Chunk'),True)
            chunked2List = parseSubtree(chunked2.subtrees(filter=lambda t: t.label() == 'Chunk'), True)
            chunked3List = parseSubtree(chunked3.subtrees(filter=lambda t: t.label() == 'Chunk'), True)

            uniqueTags = list(set(chunkedList + chunked2List + chunked3List))
            return uniqueTags


def parseSubtree(subtrees, useSyns):

    masterList = []
    for subtree in subtrees:
        treeList = list(subtree)
        #print(treeList)
        phrase = []
        if len(treeList) == 1:
                masterList.append(treeList[0])
                #print(treeList[0])
            #masterList.append(treeList[0][0])
            #masterList += addSynonyms(treeList[0][0])
        else:
            for t in treeList:
                #print(t)
                phrase.append(t[0])
                masterList.append(t)
                #masterList += addSynonyms(t[0])
            #print("PHRASE: " + str(phrase))
            lastone = treeList[len(treeList)-1][1]
            masterList.append(tuple(["_".join(phrase),lastone]))


    masterList = list(set(masterList))
    #print("**** MASTERLIST *****")
    #print(masterList)
    kingList = []

    for m in masterList:
        if m not in bad_words:
            if useSyns:
                kingList += addSynonyms(m)
            else:
                kingList.append(m[0])

    # print(masterList)
    return(list(set(kingList)))

def addSynonyms(word):

    originalWord = word[0]
    synonyms = [originalWord]
    if word[1][0] == 'N':
        originalWord += ".n.01"
    elif word[1][0] == 'J':
        originalWord += ".a.01"
    else: print("error")

    allSets = wordnet.synsets(word[0])
    if(len(allSets) == 0):
        return synonyms
    for syns in allSets:
        for syn in syns.hypernyms():
            name = syn.name().split(".")[0]
            if name not in bad_words and len(name) > 2:
                synonyms.append(name)
        for syn in syns.lemmas():
            name = syn.name()
            if name not in bad_words and len(name) > 2:
                synonyms.append(name)

    # if len(synonyms) == 0:
    #     print("found no synonyms")

    return list(set(synonyms))



if __name__ == '__main__':
    main()





