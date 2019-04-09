#import from higher
import sys
sys.path.append("..")
from InvertedIndex import build_ii
import math
import json
import string
import os
import nltk
from nltk.stem.porter import PorterStemmer as ps
from nltk import sent_tokenize 
from nltk.corpus import stopwords 
from nltk import word_tokenize 
from collections import defaultdict
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

    
uottawa_json = os.path.dirname(os.path.join(os.getcwd()))+"/Json_data/uottawa_corpus.json"
reuters_json = os.path.dirname(os.path.join(os.getcwd()))+"/Json_data/final_reuters_corpus.json"
dict_json = os.path.dirname(os.path.join(os.getcwd()))+"/Json_data/final_dict.json"  



class VSM():
    def __init__(self, inv_index):
        with open(uottawa_json) as uo_corpus, open(reuters_json) as reuters_corpus:
            uottawaC = json.load(uo_corpus)
            reutersC = json.load(reuters_corpus)
            self.complete_set = {document['doc_id'] for document in uottawaC}
            self.complete_set |= {document['doc_id'] for document in reutersC}
        self.inverted_index = inv_index
        self.mode = 'fullText'

    def retrieve(self, query, mode):
        query = to_lower(query)
        self.mode = mode
        if mode == 'alteredText':
            query = normalize(ps(stopwords_removal(query)))
        elif mode == 'normalized':
            query = normalize(query)
        elif mode == 'stemmed':
            query = stemming(query)
        elif mode == 'stopWord':
            query = stopwords_removal(query)

        tokens = word_tokenize(query)
        query_vector = [1] * len(tokens)

        self.tf_idf_matrix = tf_idf_calc( self.complete_set, self.inverted_index[self.mode], idf_calc(self.complete_set, self.inverted_index[self.mode]))

        doc_vectors = tf_idf_weight(self.complete_set, self.tf_idf_matrix, tokens)

        return document_score(query_vector, doc_vectors)
#inverted inex for the words.
def idf_calc(complete_set, inverted_index):
    total_docs = len(complete_set)
    return {word: math.log10(total_docs / len(docs))
            for word, docs in inverted_index.items()}
#Word over document frequency 
def tf_idf_calc(complete_set, inverted_index, idf_index):
    tf_idf = defaultdict(lambda: defaultdict(int))
    for word, docs in inverted_index.items():
        placeholder = defaultdict(int)
        for doc_id in complete_set:
            placeholder[doc_id] = 0
        for appearance in docs:
            placeholder[appearance.doc_id] = appearance.frequency * \
                idf_index[word]
        tf_idf[word] = placeholder
    return tf_idf
#weigh of each word in the query based on tf_idf
def tf_idf_weight(complete_set, tf_idf_matrix, tokens):
    doc_vectors = defaultdict(tuple)
    for doc_id in complete_set:
        vector = []
        for token in tokens:
            set_of_docweights = tf_idf_matrix[token]
            weight = set_of_docweights[doc_id]
            vector.append(weight)
        doc_vectors[doc_id] = vector
    return doc_vectors

#score for each document
def document_score(query_vector, doc_vectors):
    scores = []
    for doc_id, vector in doc_vectors.items():
        score = 0
        for query_vector_weight, doc_tf_idf in zip(query_vector, vector):
            score += query_vector_weight * doc_tf_idf
        scores.append((doc_id, score))
    scores.sort(key=lambda tup: tup[1], reverse=True)
    return [score for score in scores if score[1] != 0]
