import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import state_union
from nltk.stem import PorterStemmer
from nltk.tokenize import PunktSentenceTokenizer

# TOKENIZING

example_sentence = "Latoya Garrett, Event \u0026 Marketing Strategist and also known as \"The Event Storyteller\" helps creative entrepreneurs and literary professionals enhance their brand, attract the right audience and create unforgettable experiences by hosting live events worth attending that tell their brand story. Together we focus on event strategies and promotion, literary marketing, sponsorship/vendor procurement, and experential execution."
stop_words = set(stopwords.words('english'))
word_tokens = word_tokenize(example_sentence)

filtered_sentence = [w for w in word_tokens if not w in stop_words]
for w in word_tokens:
    if w not in stop_words:
        filtered_sentence.append(w)

#print(word_tokens)
print(filtered_sentence)


# POS TAGGING
train_text = state_union.raw("2005-GWBush.txt")
sample_text = state_union.raw("2006-GWBush.txt")
sample_sentence = "Latoya Garrett, Event Marketing Strategist and also known as The Event Storyteller helps creative entrepreneurs and literary professionals enhance their brand, attract the right audience and create unforgettable experiences by hosting live events worth attending that tell their brand story. Together we focus on event strategies and promotion, literary marketing, sponsorship/vendor procurement, and experential execution."

custom_sent_tokenizer = PunktSentenceTokenizer(train_text)
tokenized = custom_sent_tokenizer.tokenize(sample_text)

def process_content():
    try:
        for i in tokenized[:5]:
            words = nltk.word_tokenize(i)
            tagged = nltk.pos_tag(words)
            all_words = []
            for w in words:
                all_words.append(w.lower())
            all_words = nltk.FreqDist(all_words)
            print(list(all_words.keys()[:50]))
            namedEnt = nltk.ne_chunk(tagged, binary=False)
            namedEnt.draw()
            # chunkGram = r"""Chunk: {<RB.?>*<VB.?>*<NNP>+<NN>?}"""
            # chunkParser = nltk.RegexpParser(chunkGram)
            # chunked = chunkParser.parse(tagged)
            # chunked.draw()

            #print(tagged)


    except Exception as e:
        print(str(e))


process_content()




