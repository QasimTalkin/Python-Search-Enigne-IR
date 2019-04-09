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
#building inverted index /Users/Qasim/Desktop/Dev/WebDev/Projects /Js Python/Python-Search-Enigne-IR/
uottawa_json = "/Users/Qasim/Desktop/Dev/WebDev/Projects /Js Python/Python-Search-Enigne-IR/Model/Json_data/uottawa_corpus.json"
reuters_json = "/Users/Qasim/Desktop/Dev/WebDev/Projects /Js Python/Python-Search-Enigne-IR/Model/Json_data/final_reuters_corpus.json"
dict_json = "/Users/Qasim/Desktop/Dev/WebDev/Projects /Js Python/Python-Search-Enigne-IR/Model/Json_data/final_dict.json"  

class BuildII():
#build inverted index from dictionary files we have inverted index for each 
#Dictionary like Full text, Altered Text, Stemmed, stopwords removal, normalized 
#We will used both our corpus files and dictionary corpus to build the inverted index!
    
#loading uottawa json 
    def __init__(self):
        with open(uottawa_json) as corpus:
            self.uo_corpus = json.load(corpus)
    #loading reuters json 
        with open(reuters_json) as corpus:
            self.reuters_corpus = json.load(corpus)
    #loading dictionary json 
        with open(dict_json) as dictionary:
            self.dict_corpus = json.load(dictionary)
#Using list as the default_factory, it is easy to group a sequence of key-value pairs into a dictionary of lists:
#   >>> s = [('yellow', 1), ('blue', 2), ('yellow', 3), ('blue', 4), ('red', 1)]
#   >>> d = defaultdict(list)
#   >>> for k, v in s:
#   ...     d[k].append(v)
#   ...
#   >>> d.items()
#   [('blue', [2, 4]), ('red', [1]), ('yellow', [1, 3])]
    def make_inverted_index(self):
        print("------------Inverted Index------------")
        inv_index = defaultdict(list)
        count = 0
        for index, corpus in enumerate ([self.reuters_corpus, self.uo_corpus]):
            for doc in corpus:
                bow = set(to_lower(word)for word in word_tokenization(doc['title']) if word not in string.punctuation and not any(i.isdigit() for i in word) and word != "")
                bow |= set(to_lower(word)for word in word_tokenization(doc['description']) if word not in string.punctuation and not any(i.isdigit() for i in word) and word != "")
                count=count+1
                print("bow", count)
#we count bag of words!        
            for word in bow:
                if word_in(doc['description'], word) or word_in(doc['title'], word):
                    count = sum(1 for _ in re.finditer(r'\b%s\b' %
                                                        re.escape(to_lower(word)), to_lower(doc['description']))) + sum(1 for _ in re.finditer(r'\b%s\b' %re.escape(to_lower(word)), to_lower(doc['title'])))
                    docCount = DocCount(doc['doc_id'], count)
                    inv_index[word].append(docCount)

        #with open('inverted_index.json', 'w') as outfile:
            #json.dump(inv_index, outfile, ensure_ascii=False, indent=4)
        print("------------Done------------")
        return inv_index

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
