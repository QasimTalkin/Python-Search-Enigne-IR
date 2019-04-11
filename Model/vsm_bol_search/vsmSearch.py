from collections import defaultdict
import math
import sys
from functools import reduce
from nltk import word_tokenize as wt
import json
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer  as ps
from timeit import default_timer as timer

#dictionary and term dictionary
dictionary = set()
postings = defaultdict(dict)
#length doc_id with "euclidean length of the corresponding vector"
length = defaultdict(float)
#document frequency:-terms, with
#corresponding values equal to the number of documents
document_frequency = defaultdict(int)


#Loading or corpus
complete_json =  '/Users/Qasim/Desktop/Dev/WebDev/Projects /Js Python/Python-Search-Enigne-IR/Model/Json_data/complete_corpus.json'
with open(complete_json, encoding='utf8') as corpus:
            document_filenames = json.load(corpus)  

N = len(document_filenames)
def main():
    print("--------------------Term Frequency----------------")
    start1=timer()
    start = timer()
    initialize_terms_and_postings()
    end = timer()
    print(f'----------------Took {end-start}-----------------')
    print("---------------------Document Frequency-----------------")
    start = timer()
    initialize_document_frequencies()
    end = timer()
    print(f'----------------Took {end-start}-----------------')
    print("--------------------Length Calc-------------------")
    start = timer()
    initialize_lengths()
    end = timer()
    end1= timer()
    print(f'------Complete---Took {end1-start1}-----------------')

    while True:
        do_search()



#for each doc in corpus we split ti into terms and addd new twerms to global dic
#and add and freq ito posting list. 
def initialize_terms_and_postings():
    global dictionary, postings
    for id in document_filenames:
        terms = wt(id['description'])
        terms = terms + (wt(id['title']))
        #terms = ps(terms)
        unique_terms = set(terms)
        dictionary = dictionary.union(unique_terms)
        for term in unique_terms:
            postings[term][id['doc_id']] = terms.count(term)
            #print(postings[term][id['doc_id']])
    #print(postings)
    #return postings

 #For each document how many time the "term" appears send it to document_frequency[term]  
def initialize_document_frequencies():
    for term in dictionary:
        document_frequency[term] = len(postings[term])
    #print(document_frequency)

#find length of each document for cosine similarities ! 
def initialize_lengths():
    """Computes the length for each document."""
    global length
    count=0
    for id in document_filenames:
        count=count+1
        k = id['doc_id']
        print(f'working on document {count} ->>>>>>>> {k}')
        l = 0
        for term in dictionary:
            l += imp(term,id['doc_id'])**2
        length[id['doc_id']] = math.sqrt(l)
    with open('doc_length.json', 'w') as outfile:
        json.dump(length, outfile)
#Importance of term in document! if not give me 0
def imp(term,id):
    """Returns the importance of term in document id.  If the term
    isn't in the document, then return 0."""
    if id in postings[term]:
        return postings[term][id]*inverse_document_frequency(term)
    else:
        return 0.0
def inverse_document_frequency(term):
    if term in dictionary:
        return math.log(N/document_frequency[term],2)
    else:
        return 0.0
#Return documents with decreasing cosine similarities 
def do_search():

    query = wt(input("Search query >> "))
    if query == []:
        sys.exit()
    # find document ids containing all query terms.  Works by
    # intersecting the posting lists for all query terms.
    print("\n\n\n",[set(postings[term].keys()) for term in query],"\n\n\n")
    relevant_document_ids = intersection([set(postings[term].keys()) for term in query])
    list(relevant_document_ids)
    if not relevant_document_ids:
        print ("No documents matched all query terms.")
    else:
        scores = sorted([(id,similarity(query,id)) 
                         for id in relevant_document_ids],
                        key=lambda x: x[1],
                        reverse=True)
        print ("Score: filename")
        for (id,score) in scores:
           print (str(score)+": "+id) 
#Intersection of two given sets is the largest set which contains all the elements that are common to both the sets.
def intersection(sets):
    """Returns the intersection of all sets in the list sets. Requires
    that the list sets contains at least one element, otherwise it
    raises an error."""
    return reduce(set.intersection, [s for s in sets])


#cosine between query and document 
def similarity(query,id):
    similarity = 0.0
    for term in query:
        if term in dictionary:
            similarity += inverse_document_frequency(term)*imp(term,id)
    similarity = similarity / length[id]
    
    return similarity





if __name__ == "__main__":
        main()
