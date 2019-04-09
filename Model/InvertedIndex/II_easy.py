from sklearn.feature_extraction.text import TfidfVectorizer
import json
import pandas as pd
import os
from scipy.sparse.csr import csr_matrix 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer




def stemming (): 
    stemmer = SnowballStemmer("english")
    df['stemmed'] = df.document.map(lambda x: ' '.join([stemmer.stem(y) for y in x.decode('utf-8').split(' ')]))
    df.stemmed.head()

def tf_idf_vector():
# Starting with the CountVectorizer/TfidfTransformer approach...
    cvec = CountVectorizer(stop_words='english', min_df=1, max_df=.5, ngram_range=(1,2))
    cvec

def main():
    uottawa_json = os.path.dirname(os.path.join(os.getcwd()))+"/Json_data/uottawa_corpus.json"
    reuters_json = os.path.dirname(os.path.join(os.getcwd()))+"/Json_data/final_reuters_corpus.json"
    corpus_collection = [uottawa_json, reuters_json]

    for id, corpus_data in enumerate(corpus_collection):
        with open(corpus_data) as corpus:
            data = json.load(corpus)

    complete_set = {document['doc_id'] for document in data}
    complete_set |= {document['description'] for document in data}

    pjson = pd.read_json(uottawa_json)
    pjson = pjson.append(pd.read_json(reuters_json))

    tf = TfidfVectorizer()
    tfidf_matrix = tf.fit_transform(pjson)
    feature_names = tf.get_feature_names()
    doc = 0
    feature_index = tfidf_matrix[doc,:].nonzero()[1]
    tfidf_scores = zip(feature_index, [tfidf_matrix[doc, x] for x in feature_index])
    print(tf.vocabulary_)


        
    #df = pd.DataFrame(X.toarray(), columns = tf.get_feature_names())



if __name__ == '__main__':
    main()




