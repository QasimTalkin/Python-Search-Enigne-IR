import string
from nltk.stem.porter import PorterStemmer as ps
from nltk import sent_tokenize 
from nltk.corpus import stopwords 
from nltk import word_tokenize as wt

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
