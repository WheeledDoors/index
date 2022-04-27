from gensim.models import Word2Vec
import requests
import json
import time
import praw
import pandas as pd
import os
from bs4 import BeautifulSoup
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from gensim import corpora
import gensim

def handler(event, context):
    print("Received event: " + str(event))

    # print('## ENVIRONMENT VARIABLES')
    # print(os.environ)

    setup_nltk_dir()

    tres1, rres1, wres1, tnb1, rnb1, tlda1, rlda1  = search(event['word1'])
    # tres2, rres2, wres2 = search(event['word2'])

    data = {}
    data['word1'] = {}
    # data['word2'] = {}

    data['word1']['related_words'] = {}
    data['word1']['related_words']['wiki'] = wres1
    data['word1']['related_words']['twit'] = tres1
    data['word1']['related_words']['redd'] = rres1
    # data['word1']['related_words']['redd'] = [('dummy', 0.5)]  # TODO Remove

    # data['word2']['related_words'] = {}
    # data['word2']['related_words']['wiki'] = wres2
    # data['word2']['related_words']['twit'] = tres2
    # # data['word2']['related_words']['redd'] = rres2
    # data['word2']['related_words']['redd'] = [('dummy', 0.5)]  # TODO Remove

    # TODO Change placeholder
    # data['word1']['sentiment'] = [0.75, 0.25, 75, 25, 25, 75]
    data['word1']['sentiment'] = [tnb1[0], rnb1[0], tnb1[1], tnb1[2], rnb1[1], rnb1[2]]
    # data['word2']['sentiment'] = [0.25, 0.75, 25, 75, 75, 25]

    data['word1']['topic'] = {}
    # data['word2']['topic'] = {}

    # data['word1']['topic']['wiki'] = wlda1
    data['word1']['topic']['redd'] = rlda1
    data['word1']['topic']['twit'] = tlda1
    # data['word2']['topic']['wiki'] = dummy_topics2
    # data['word2']['topic']['redd'] = dummy_topics3
    # data['word2']['topic']['twit'] = dummy_topics4

    return {
        'statusCode': 200,
        'body': json.dumps(data)
    }


def get_tweets(search, num_tweets=5):

    with open('key.json') as f:
        key = json.load(f)
        bearer_token = key['BEARER_TOKEN']

    # Create the url
    url = 'https://api.twitter.com/1.1/search/tweets.json?result_type=popular&q=' + \
        search + '&max_results=' + str(num_tweets)
    # Create request headers
    headers = {
        'authorization': 'Bearer ' + bearer_token,
        'user-agent': 'v2FilteredStreamPython',
    }
    # Make the request
    response = requests.get(url, headers=headers)
    return response.json()


def get_wikipedia_data(search, num_posts=5):
    # Create the url for the search also get the posts text
    url = 'https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch=' + \
        search + '&format=json&srlimit=' + str(num_posts)
    # Make the request
    response = requests.get(url)
    return response.json()


def split_into_sentences(text):
    out = []
    for sentence in text:
        sentence = sentence.split()
        out.append(sentence)
    return out


def setup_nltk_dir():
    print('## SETUP NLTK DIR')
    cwd = os.getcwd()
    print(cwd)
    nltk.data.path.append(cwd + '/nltk_data')


def setup_df_clean(text_list):
    df = pd.Series(text_list)
    # print(df)
    # Remove any rows with NA values
    return df


def search(word):
    print('## SEARCHING FOR: ' + word)
    # Get tweets
    print("### Getting TWEETS")
    tweets_data = get_tweets(word, 100)
    tweets_text = [x["text"] for x in tweets_data["statuses"]]

    print("### Getting Reddit")
    # Get reddit # TODO Bring back
    reddit = praw.Reddit(
        client_id="r3dlLRYKcBN9-JRoyvi1Xw",
        client_secret="YfKwRqhLjS1darC2TL5QnrzDe0S_sQ",
        user_agent="hiiiiiiiiii",
    )
    reddit_data = reddit.subreddit("all").search(word, limit=200)
    reddit_text = [x.title for x in reddit_data]

    print("### Getting Wiki")
    # Get wikipedia
    wiki_search = get_wikipedia_data(word, 50)
    wiki_text = []
    for page in wiki_search['query']['search']:
        url = 'https://en.wikipedia.org/wiki/' + page['title']
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # file_name = '/tmp/data/wiki/' + page['title'] + '.txt'
        # Make file name compatible with windows
        # file_name = file_name.replace(' ', '_').replace(':', '_').replace('\\', '_').replace('"', '_').replace('?', '_').replace('*', '_').replace('|', '_').replace('<', '_').replace('>', '_')
        # with open(file_name, 'w') as f:
        # 	f.write(soup.get_text())
        text = soup.get_text()
        for _ in range(100):
            text = text.replace('\n\n', '\n')
        wiki_text.append(text)
        time.sleep(0.01)

        # files_wiki = glob.glob('/tmp/data/wiki/*.txt')
        # wiki_text = []
        # for f in files_wiki:
        # 	with open(f, 'r') as f:
        # 		text = f.read()
        # 		# remove duplicate \n
        # 		for _ in range(100):
        # 			text = text.replace('\n\n', '\n')
        # 		wiki_text.append(text)

    ### SETUP SENTIMENT ANALYSIS ###

    print('## SENTIMENT ANALYSIS')
    # print(tweets_text)
    # print(wiki_text)

    twit_df = setup_df_clean(tweets_text)
    redd_df = setup_df_clean(reddit_text) # TODO Bring back
    # wiki_df = setup_df_clean(wiki_text)

    # print('## DFs')
    # print(twit_df)
    # print(reddit_df) # TODO Bring back
    # print(wiki_df)

    # Split into sentences
    tweets_text = split_into_sentences(tweets_text)
    reddit_text = split_into_sentences(reddit_text) # TODO Bring back
    wiki_text = split_into_sentences(wiki_text)

    ### RUN SENTIMENT THINGS ###
    twit_nb = NB_BOW(twit_df)
    redd_nb = NB_BOW(redd_df) # TODO Bring back
    # wiki_nb = NB_BOW(wiki_df)

    print('## LDA')
    twit_lda = LDA(twit_df, 3)
    redd_lda = LDA(redd_df, 3) # TODO Bring back
    # wiki_lda = LDA(wiki_df, 3)

    print(twit_nb)
    print(redd_nb) # TODO Bring back
    # print(wiki_nb)

    ### RUN IF YOU \ ##

    # model_twitter = Word2Vec.load("models/glove_twitter.model")
    # model_reddit = Word2Vec.load("models/glove_twitter.model")
    # model_wiki = Word2Vec.load("models/glove_wiki_gigaword.model")

    print("## LOADING MODELS")
    model_twitter = Word2Vec.load("models/base.model")
    model_reddit = Word2Vec.load("models/base.model") # TODO Bring back
    model_wiki = Word2Vec.load("models/base.model")

    print("## TRAINING MODELS")
    # Train the model
    model_twitter.train(
        tweets_text, total_examples=len(tweets_text), epochs=10)
    model_reddit.train(reddit_text, total_examples=len(reddit_text), epochs=10) # TODO Bring back
    model_wiki.train(wiki_text, total_examples=len(wiki_text), epochs=10)

    twitter_top = model_twitter.wv.most_similar(word, topn=10)
    reddit_top = model_reddit.wv.most_similar(word, topn=10) # TODO Bring back
    wiki_top = model_wiki.wv.most_similar(word, topn=10)
    # print(word + " twitter: " + str(twitter_top))
    # print(word + " reddit: " + str(reddit_top))
    # print(word + " wiki: " + str(wiki_top))

    # Print the length of the results
    # print("## LENGTHS")
    # print("Twitter: " + str(len(twitter_top)))
    # print("Reddit: " + str(len(reddit_top))) # TODO Bring back
    # print("Wiki: " + str(len(wiki_top)))

    # reddit_top = ['aaa']

    return twitter_top, reddit_top, wiki_top, twit_nb, redd_nb, twit_lda, redd_lda


def clean_data(df):
    lemmatizer = WordNetLemmatizer()
    stop_words = pickle.load(open("stop_words.pickle", 'rb'))

    df = df.apply(word_tokenize)
    df = df.map(lambda x: [i.lower()
                for i in x if i.lower() not in stop_words])
    df = df.map(lambda x: [lemmatizer.lemmatize(i)
                for i in x if i.lower() if i.isalnum()])
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
    ldamodel = Lda(doc_term_matrix, num_topics=n_topics,
                   id2word=dictionary, passes=50)

    my_dict = {'Topic_' + str(i): [token for token, score in ldamodel.show_topic(i, topn=10)] for i in
               range(0, ldamodel.num_topics)}

    print(my_dict)
    return my_dict


def NB_BOW(df):
    vect = pickle.load(open("BOW_Vect", 'rb'))
    loaded_model = pickle.load(open("NB_BOW.sav", 'rb'))
    df = clean_data(df)
    x_vec = vect.transform(df)
    result = loaded_model.predict(x_vec)
    return [np.mean(result), len(np.where(result == 0)[0]), len(np.where(result == 1)[0])]


def Log_TFIDF(df):
    vect = pickle.load(open("TFIDF.sav", 'rb'))
    loaded_model = pickle.load(open("Log_TFIDF.sav", 'rb'))
    df = clean_data(df)
    x_vec = vect.transform(df)
    result = loaded_model.predict(x_vec)
    return [np.mean(result), len(np.where(result == 0)[0]), len(np.where(result == 1)[0])]
