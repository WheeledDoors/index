import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import nltk
import pickle


from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

# Importing Gensim
import gensim
from gensim import corpora



def clean_data(df):
    lemmatizer = WordNetLemmatizer()
    stop_words = pickle.load(open("stop_words.pickle", 'rb'))

    df = df.apply(word_tokenize)
    df = df.map(lambda x: [i.lower() for i in x if i.lower() not in stop_words])
    df = df.map(lambda x: [lemmatizer.lemmatize(i) for i in x if i.lower() if i.isalnum()])
    df = df.map(lambda x: ' '.join(x))
    return df


def LDA(df, n_topics):
    df = clean_data(df)

    # preprocessing
    doc_clean = [i.split() for i in df]
    dictionary = corpora.Dictionary(doc_clean)
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]

    # Build model:
    Lda = gensim.models.ldamodel.LdaModel
    ldamodel = Lda(doc_term_matrix, num_topics=n_topics, id2word=dictionary, passes=50)

    my_dict = {'Topic_' + str(i): [token for token, score in ldamodel.show_topic(i, topn=10)] for i in
               range(0, ldamodel.num_topics)}

    return my_dict


def NB_BOW(df):
    vect = pickle.load(open("BOW_Vect", 'rb'))
    loaded_model = pickle.load(open("NB_BOW.sav", 'rb'))
    df = clean_data(df)
    x_vec = vect.transform(df)
    result = loaded_model.predict(x_vec)
    return result


def Log_TFIDF(df):
    vect = pickle.load(open("TFIDF.sav", 'rb'))
    loaded_model = pickle.load(open("Log_TFIDF.sav", 'rb'))
    df = clean_data(df)
    x_vec = vect.transform(df)
    result = loaded_model.predict(x_vec)
    return result