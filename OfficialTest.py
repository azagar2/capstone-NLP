import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import PunktSentenceTokenizer
from nltk.tree import Tree
import json


# STOP WORDS
stop_words = set(stopwords.words('english'))


def main():

    # IMPORT DATA FROM JSON FILE
    with open('data.json') as json_data:
        data = json.load(json_data)

    # Master arrays
    #master_titles =

    # Go through all data (titles for now)
    for event in data[8:9]:
        print(event['title'])
        title = event['title']
        category = event['category_key']
        print(category)
        example_sentence = event['description']
        example_sentence = example_sentence.lower()

        # Use Punkt Tokenizer - TITLE
        process_title(title)

        # Use Punkt Tokenizer - CONTENT
        custom_sent_tokenizer = PunktSentenceTokenizer(example_sentence)
        tokenized = custom_sent_tokenizer.tokenize(example_sentence)
        process_content(tokenized)


#################################

def process_title(title):
    words = nltk.word_tokenize(title)
    filtered_sentence = []
    for w in words:
        if w not in stop_words:
            filtered_sentence.append(w)
    tagged = nltk.pos_tag(filtered_sentence)
    namedEntTrue = nltk.ne_chunk(tagged, binary=True)
    namedEntFalse = nltk.ne_chunk(tagged, binary=False)
    #namedEntFalse.draw()
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


    # print(named_entities)
    # print(named_entities_false)

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
            master_titles.append(" ".join(temp))

    if len(named_entities) > 0:
        for item in named_entities:
            master_titles.append(item[0])


    # print(named_entities)
    # print(named_entities_false)
    if len(master_titles) > 0:
        print(set(master_titles))


def process_content(tokenized):
    try:
        for i in tokenized[:]: #tokenized[:3]
            words = nltk.word_tokenize(i)
            #filtered_sentence = [w for w in words if not w in stop_words]
            filtered_sentence = []
            for w in words:
                if w not in stop_words:
                    filtered_sentence.append(w)
            tagged = nltk.pos_tag(filtered_sentence) #words
            chunkParser = nltk.RegexpParser(r"""Chunk: {<J.+>+<N.+>?}""")
            chunkParser2 = nltk.RegexpParser(r"""Chunk: {<JJ>*<NN>}""")
            chunkParser3 = nltk.RegexpParser(r"""Chunk: {<NN.*>+}""")
            chunked = chunkParser.parse(tagged)
            chunked2 = chunkParser2.parse(tagged)
            chunked3 = chunkParser3.parse(tagged)
            #chunked.draw()

            # if len(tokenized) == 1:
            #     chunked.draw()

            #for subtree in chunked.subtrees(filter=lambda t: t.label() == 'Chunk'):
                # print(list(subtree))

            # print(parseSubtree(chunked.subtrees(filter=lambda t: t.label() == 'Chunk')))
            #
            # print('+++++++++++++++++++')
            #
            # print(parseSubtree(chunked2.subtrees(filter=lambda t: t.label() == 'Chunk')))

            #for subtree in chunked2.subtrees(filter=lambda t: t.label() == 'Chunk'):
                # print(list(subtree))

            # print('+++++++++++++++++++')

            #for subtree in chunked3.subtrees(filter=lambda t: t.label() == 'Chunk'):
                #print(list(subtree))

            #print(parseSubtree(chunked3.subtrees(filter=lambda t: t.label() == 'Chunk')))

            chunkedList = parseSubtree(chunked.subtrees(filter=lambda t: t.label() == 'Chunk'))
            chunked2List = parseSubtree(chunked2.subtrees(filter=lambda t: t.label() == 'Chunk'))
            chunked3List = parseSubtree(chunked3.subtrees(filter=lambda t: t.label() == 'Chunk'))

            uniqueTags = set(chunkedList + chunked2List + chunked3List)
            print(uniqueTags)

            print('=====================')



            print('========********=========')


    except Exception as e:
        print(str(e))


def parseSubtree(subtrees):

    masterList = []
    for subtree in subtrees:
        treeList = list(subtree)
        #print(treeList)
        phrase = []
        if len(treeList) == 1:
            masterList.append(treeList[0][0])
        else:
            for t in treeList:
                phrase.append(t[0])
                masterList.append(t[0])
            masterList.append(" ".join(phrase))
    return(masterList)


def get_continuous_chunks(text):
    chunked = nltk.ne_chunk(nltk.pos_tag(word_tokenize(text)))
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



if __name__ == '__main__':
    main()





