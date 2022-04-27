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
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from gensim import corpora


def handler(event, context):
    print("Received event: " + str(event))

    # print('## ENVIRONMENT VARIABLES')
    # print(os.environ)

    tres1, rres1, wres1 = search(event['word1'])
    tres2, rres2, wres2 = search(event['word2'])

    data = {}
    data['word1'] = {}
    data['word2'] = {}

    data['word1']['related_words'] = {}
    data['word1']['related_words']['wiki'] = wres1
    data['word1']['related_words']['twit'] = tres1
    data['word1']['related_words']['redd'] = rres1

    data['word2']['related_words'] = {}
    data['word2']['related_words']['wiki'] = wres2
    data['word2']['related_words']['twit'] = tres2
    data['word2']['related_words']['redd'] = rres2

    data['word1']['sentiment'] = [0.75, 75, 25]
    data['word2']['sentiment'] = [0.25, 25, 75]

    dummy_topics = {'Topic_0': ['br',
                                'product',
                                'would',
                                'amazon',
                                'flavor',
                                'like',
                                'buy',
                                'taste',
                                '2',
                                'tbsp'],
                    'Topic_1': ['br',
                                'tea',
                                'like',
                                'one',
                                'good',
                                'flavor',
                                'also',
                                'make',
                                'taste',
                                'magnesium'],
                    'Topic_2': ['coffee',
                                'br',
                                'flavor',
                                'product',
                                'cup',
                                'get',
                                'would',
                                'taste',
                                'good',
                                'tea'],
                    'Topic_3': ['br',
                                'like',
                                'food',
                                'taste',
                                'good',
                                'love',
                                'dog',
                                'great',
                                'really',
                                'eat'],
                    'Topic_4': ['br',
                                'good',
                                'coffee',
                                'product',
                                'like',
                                'would',
                                'store',
                                'chip',
                                'great',
                                'price']}

    dummy_topics2 = dummy_topics.copy()
    dummy_topics2['Topic_0'][0] = 'weewoo'
    dummy_topics3 = dummy_topics.copy()
    dummy_topics3['Topic_0'][0] = 'apple'
    dummy_topics4 = dummy_topics.copy()
    dummy_topics4['Topic_0'][0] = 'banana'

    data['word1']['topic'] = {}
    data['word2']['topic'] = {}

    data['word1']['topic']['wiki'] = dummy_topics
    data['word1']['topic']['redd'] = dummy_topics2
    data['word1']['topic']['twit'] = dummy_topics3
    data['word2']['topic']['wiki'] = dummy_topics2
    data['word2']['topic']['redd'] = dummy_topics3
    data['word2']['topic']['twit'] = dummy_topics4

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


def search(word):
    print('## SEARCHING FOR: ' + word)
    # Get tweets
    tweets_data = get_tweets(word, 100)
    tweets_text = [x["text"] for x in tweets_data["statuses"]]

    # Get reddit
    reddit = praw.Reddit(
        client_id="r3dlLRYKcBN9-JRoyvi1Xw",
        client_secret="YfKwRqhLjS1darC2TL5QnrzDe0S_sQ",
        user_agent="hiiiiiiiiii",
    )
    reddit_data = reddit.subreddit("all").search(word, limit=1000)
    reddit_text = [x.title for x in reddit_data]

    # Get wikipedia
    wiki_search = get_wikipedia_data(word, 100)
    text_wiki = []
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
        text_wiki.append(text)
        time.sleep(0.01)

        # files_wiki = glob.glob('/tmp/data/wiki/*.txt')
        # text_wiki = []
        # for f in files_wiki:
        # 	with open(f, 'r') as f:
        # 		text = f.read()
        # 		# remove duplicate \n
        # 		for _ in range(100):
        # 			text = text.replace('\n\n', '\n')
        # 		text_wiki.append(text)

    # Split into sentences
    tweets_text = split_into_sentences(tweets_text)
    reddit_text = split_into_sentences(reddit_text)
    text_wiki = split_into_sentences(text_wiki)

    ### RUN SENTIMENT ANALYSIS ###

    print('## SENTIMENT ANALYSIS')
    twit_df = pd.DataFrame(tweets_text)
    redd_df = pd.DataFrame(reddit_text)
    wiki_df = pd.DataFrame(text_wiki)

    twit_nb = NB_BOW(twit_df)
    redd_nb = NB_BOW(redd_df)
    wiki_nb = NB_BOW(wiki_df)

    print(twit_nb)
    print(redd_nb)
    print(wiki_nb)

    ### RUN IF YOU \ ##

    # model_twitter = Word2Vec.load("models/glove_twitter.model")
    # model_reddit = Word2Vec.load("models/glove_twitter.model")
    # model_wiki = Word2Vec.load("models/glove_wiki_gigaword.model")

    print("## LOADING MODELS")
    model_twitter = Word2Vec.load("models/base.model")
    model_reddit = Word2Vec.load("models/base.model")
    model_wiki = Word2Vec.load("models/base.model")

    print("## TRAINING MODELS")
    # Train the model
    model_twitter.train(
        tweets_text, total_examples=len(tweets_text), epochs=10)
    model_reddit.train(reddit_text, total_examples=len(reddit_text), epochs=10)
    model_wiki.train(text_wiki, total_examples=len(text_wiki), epochs=10)

    twitter_top = model_reddit.wv.most_similar(word, topn=10)
    reddit_top = model_reddit.wv.most_similar(word, topn=10)
    wiki_top = model_wiki.wv.most_similar(word, topn=10)
    # print(word + " twitter: " + str(twitter_top))
    # print(word + " reddit: " + str(reddit_top))
    # print(word + " wiki: " + str(wiki_top))

    # Print the length of the results
    print("## LENGTHS")
    print("Twitter: " + str(len(twitter_top)))
    print("Reddit: " + str(len(reddit_top)))
    print("Wiki: " + str(len(wiki_top)))

    return twitter_top, reddit_top, wiki_top


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
