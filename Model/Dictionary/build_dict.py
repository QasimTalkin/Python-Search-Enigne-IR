import json
import string
import nltk
import os
from nltk.corpus import stopwords as sw
from nltk.tokenize import word_tokenize as wt
from nltk.stem.porter import PorterStemmer as ps
#Normalizing Text 
def normalize(obj):
    return {words.translate(str.maketrans('', '', string.punctuation)).lower() for words in obj}
#stopword removal 
def remove_stopwords(text):
    stop_words = set(sw.words('english')) | set(
        sw.words('french'))
    return set([w.lower() for w in text if not w in stop_words])
def stemming(obj):
    stem = ps()
    return set([stem.stem(words).lower() for words in obj])

def dict_build():
    #build dic from Uottawa an reuters json Corpus 
    #   *Full text, Altered Text, Stemmed, stopwords removal, normalized 
#Acess corpus 
    reuters_data = os.path.dirname(os.path.join(os.getcwd()))+"/Model/Pre_Processing/reuters_corpus.json"
    uottawa_data = os.path.dirname(os.path.join(os.getcwd()))+"/Model/Pre_Processing/uottawa_corpus.json"
    corpus_collection = [reuters_data, uottawa_data]
    #corpus_collection = ["reuters_corpus.json", "uottawa_corpus.json"]
#Dictionary Json Structure 
    dict = {
            'fullText': set(),
            'alteredText': set(),
            'stemmedText': set(),
            'stopWord': set(),
            'normalized': set()
        }
#Enumerate allows us to loop over something and have an automatic counter.
#docID -> article number starting with 1
#Find title body topic create snippet
    for id, corpus_data in enumerate(corpus_collection):
        with open(corpus_data) as corpus:
            data = json.load(corpus)

            for values in data:
                tokenized_title = [word.lower()
                                       for word in wt(values['title']) if word not in string.punctuation and not any(i.isdigit() for i in word) and word != ""]
                tokenized_description = [word.lower()
                                       for word in wt(values['description']) if word not in string.punctuation and not any(i.isdigit() for i in word) and word != ""]
#dict fulltext                
                dict['fullText'] |= set(tokenized_title)
                dict['fullText'] |= set(tokenized_description)
#dict altered text [normalizing stemmed and stopwords removed title and description]
                dict['alteredText'] |= normalize(stemming(remove_stopwords(tokenized_title)))
                dict['alteredText'] |= normalize(stemming(remove_stopwords(tokenized_description)))
#stopwords removal
                dict['stopWord'] |= remove_stopwords(tokenized_title)
                dict['stopWord'] |= remove_stopwords(tokenized_description)
#stemming [porter stemmer]
                dict['stemmedText'] |= stemming(tokenized_title)
                dict['stemmedText'] |= stemming(tokenized_description)
#normalization
                dict['normalized'] |= normalize(tokenized_title)
                dict['normalized'] |= normalize(tokenized_description)

        with open('dictionary.json', 'w') as outfile:
            my_dict_lists = {k: list(v) for (k, v) in dict.items()}
            json.dump(my_dict_lists, outfile, ensure_ascii=False, indent=4)


dict_build()