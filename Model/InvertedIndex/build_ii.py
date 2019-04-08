import re
import json
from collections import defaultdict
import string
import os
from nltk.stem.porter import PorterStemmer as ps
from nltk import sent_tokenize 
from nltk.corpus import stopwords 
from nltk import word_tokenize as wt

#Text processsin. 
def to_upper(obj):
    return obj.upper()
def to_lower(obj):
    return obj.lower()
def stopwords_removal(obj):
    e_f_stop_words = set (stopwords.word('enlgish')) | set(stopwords.words('french'))
    return set([words.lower() for words in obj if not words in e_f_stop_words])
def normalize(obj):
    return {words.translate(str.maketrans('', '', string.punctuation)).lower() for words in obj}
def stemming(obj):
    stem = ps()
    return set([stem.stem(words).lower() for words in obj])
def sentence_tokenization(obj):
    return stopwords_removal(obj)
def word_tokenization(obj):
    return wt(obj)
#building inverted index
def build_inverted_index():
    print("------------Building Inverted Index------------")

#build inverted index from dictionary files we have inverted index for each 
#Dictionary like Full text, Altered Text, Stemmed, stopwords removal, normalized 
#We will used both our corpus files and dictionary corpus to build the inverted index!
    uottawa_json = os.path.dirname(os.path.join(os.getcwd()))+"/Pre_Processing/uottawa_corpus.json"
    reuters_json = os.path.dirname(os.path.join(os.getcwd()))+"/Pre_Processing/reuters_corpus.json"
    dict_json = os.path.dirname(os.path.join(os.getcwd()))+"/Dictionary/dictionary.json"  
#loading uottawa json 
    with open(uottawa_json) as corpus:
        uo_corpus = json.load(corpus)
#loading reuters json 
    with open(reuters_json) as corpus:
        reuters_corpus = json.load(corpus)
#loading dictionary json 
    with open(dict_json) as dictionary:
        dict_corpus = json.load(dictionary)
#Using list as the default_factory, it is easy to group a sequence of key-value pairs into a dictionary of lists:
#   >>> s = [('yellow', 1), ('blue', 2), ('yellow', 3), ('blue', 4), ('red', 1)]
#   >>> d = defaultdict(list)
#   >>> for k, v in s:
#   ...     d[k].append(v)
#   ...
#   >>> d.items()
#   [('blue', [2, 4]), ('red', [1]), ('yellow', [1, 3])]
    inv_index = defaultdict(list)
    for index, corpus in enumerate ([uo_corpus, reuters_corpus]):
        for doc in corpus:
            bow = set(to_lower(word)for word in word_tokenization(doc['title']) if word not in string.punctuation and not any(i.isdigit() for i in word) and word != "")
            bow |= set(to_lower(word)for word in word_tokenization(doc['description']) if word not in string.punctuation and not any(i.isdigit() for i in word) and word != "")
#we count bag of words!        
        for word in bow:
            if word_in(doc['description'], word) or word_in(doc['title'], word):
                count = sum(1 for _ in re.finditer(r'\b%s\b' %
                                                    re.escape(to_lower(word)), to_lower(doc['description']))) + sum(1 for _ in re.finditer(r'\b%s\b' %re.escape(to_lower(word)), to_lower(doc['title'])))
                docCount = DocCount(doc['doc_id'], count)
                inv_index[word].append(json.dumps(docCount.__dict__))

    with open('inverted_index.json', 'w') as outfile:
        json.dump(inv_index, outfile, ensure_ascii=False, indent=4)
    print("------------Done------------")



def word_in(fulltext, word):
    return word in fulltext
class DocCount():
    def __init__(self, doc_id, frequency):
        self.doc_id = doc_id
        self.frequency = frequency

    def __contains__(self, key):
        return key == self.doc_id

    def __repr__(self):
        return str(self.__dict__)

build_inverted_index()