import string
from nltk.stem.porter import PorterStemmer as ps
from nltk import sent_tokenize 
from nltk.corpus import stopwords
from nltk import bigrams
from nltk import word_tokenize as wt
import json
import re

def to_upper(obj):
    return obj.upper()
def lowercase(tokens):
    for t in tokens:
        yield t.lower()
def stopwords_removal(obj):
    e_f_stop_words = set (stopwords.word('english')) | set(stopwords.words('french'))
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






def generate_ngrams(s, n):
    # Convert to lowercases
    s = s.lower()
    
    # Replace all none alphanumeric characters with spaces
    s = re.sub(r'[^a-zA-Z0-9\s]', ' ', s)
    
    # Break sentence in the token, remove empty tokens
    tokens = [token for token in s.split(" ") if token != ""]
    
    # Use the zip function to help us generate n-grams
    # Concatentate the tokens into ngrams and return
    ngrams = zip(*[tokens[i:] for i in range(n)])
    return [" ".join(ngram) for ngram in ngrams]

def generate_bigrams(s):
    my_data = s
    my_data = to_lower(my_data)
    #my_data = stopwords_removal(my_data)
    my_data = normalize(my_data)
    #my_data = sent_tokenize(my_data)
    string_bigrams = bigrams(my_data)
    with open("Output.txt", "w") as text_file:
        text_file.write(string_bigrams)
    print (string_bigrams)


complete_json = '/Users/Qasim/Desktop/Dev/WebDev/Projects /Js Python/Python-Search-Enigne-IR/Model/Json_data/complete_corpus.json'
with open(complete_json) as corpus:
            DATA = json.load(corpus)
data = str(DATA)
bigram = generate_ngrams(data, n=2 )
bigram = list(dict.fromkeys(bigram))
outF = open("my_bigram.txt", "w")
for line in bigram:
  # write line to output file
  outF.write(line)
  outF.write('",\n"')
outF.close()


#generate_ngrams(DATA, n=2)
#data = [line.strip() for line in open(complete_json, 'r')]
#texts = [[word.lower() for word in text.split()] for text in data]
#bigramList = generate_ngrams(texts, 2)

#with open('complete_birgram.json', 'w') as outfile:
#    json.dump(bigramList, outfile, ensure_ascii=False, indent=5)