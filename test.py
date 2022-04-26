
import gensim.downloader as api
from gensim.models import Word2Vec
corpus = api.load('wiki-english-20171001')
model = Word2Vec(sentences=corpus, vector_size=200, window=5, min_count=1, workers=4)

model.save("models/base-wiki-english-20171001.model")

model = Word2Vec.load("models/base-wiki-english-20171001.model")

model.train([["hello", "world"]], total_examples=1, epochs=1)

vector = model.wv['computer']  # get numpy vector of a word

sims = model.wv.most_similar('computer', topn=10)  # get other similar words

print(sims)