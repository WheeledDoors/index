
import gensim.downloader as api
from gensim.models import Word2Vec
corpus = api.load('text8')
model = Word2Vec(sentences=corpus, vector_size=100, window=5, min_count=1, workers=14)

model.save("models/base.model")

model = Word2Vec.load("models/base.model")

model.train([["hello", "world"]], total_examples=1, epochs=1)

vector = model.wv['computer']  # get numpy vector of a word

sims = model.wv.most_similar('computer', topn=10)  # get other similar words

print(sims)