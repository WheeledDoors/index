import gensim.downloader

model_twitter = gensim.downloader.load("glove-twitter-25")
model_twitter.save("models/glove_twitter.model")

model_wiki = gensim.downloader.load("glove-wiki-gigaword-100")
model_wiki.save("models/glove_wiki_gigaword.model")

#model_google = gensim.downloader.load("word2vec-google-news-300")
#model_google.save("word2vec_google_news_300.model")
