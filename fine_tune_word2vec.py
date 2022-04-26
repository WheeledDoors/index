from gensim.models import Word2Vec


import loader

def split_into_sentences(text):
	out = []
	for sentence in text:
		sentence = sentence[0].split()
		out.append(sentence)
	return out

if __name__ == "__main__":
    # Load the data
	loader_twitter = loader.Twitter_Loader('data/twitter')
	twitter_wheels = loader_twitter.get_wheels_as_pandas_dataframe()
	twitter_doors = loader_twitter.get_doors_as_pandas_dataframe()
	loader_reddit = loader.Reddit_Loader('data/reddit')
	reddit_wheels = loader_reddit.get_wheels_as_pandas_dataframe()
	reddit_doors = loader_reddit.get_doors_as_pandas_dataframe()
	loader_wiki = loader.wiki_Loader('data/wiki')
	wiki_wheels = loader_wiki.get_wheels_as_pandas_dataframe()
	wiki_doors = loader_wiki.get_doors_as_pandas_dataframe()
 
	# Convert to list of strings
	twitter_wheels_list = twitter_wheels.values.tolist()
	twitter_doors_list = twitter_doors.values.tolist()
	reddit_wheels_list = reddit_wheels.values.tolist()
	reddit_doors_list = reddit_doors.values.tolist()
	wiki_wheels_list = wiki_wheels.values.tolist()
	wiki_doors_list = wiki_doors.values.tolist()
	
	# Split into words
	twitter_wheels_list = split_into_sentences(twitter_wheels_list)
	twitter_doors_list = split_into_sentences(twitter_doors_list)
	reddit_wheels_list = split_into_sentences(reddit_wheels_list)
	reddit_doors_list = split_into_sentences(reddit_doors_list)
	wiki_wheels_list = split_into_sentences(wiki_wheels_list)
	wiki_doors_list = split_into_sentences(wiki_doors_list)
	# model_twitter = api.load("glove-twitter-25")	
	# print(type(model_twitter))
	# corpus = api.load('text8')
	# Fine-tune the word2vec model
	# model_twitter = Word2Vec(sentences=corpus, vector_size=100, window=5, min_count=1, workers=4)
	# model_twitter.save('models/base.model')
	model_twitter = Word2Vec.load('models/base.model')
	# model_twitter = Word2Vec.load('models/base.model')
	model_twitter.train(twitter_wheels_list + twitter_doors_list, total_examples=len(twitter_wheels_list + twitter_doors_list), epochs=10)
	print("Door twitter: " + str(model_twitter.wv.most_similar('door', topn=10)))
	print("Wheel twitter: " + str(model_twitter.wv.most_similar('wheel', topn=10)))
	model_reddit = Word2Vec.load('models/base.model')
	model_reddit.train(reddit_wheels_list + reddit_doors_list, total_examples=len(reddit_wheels_list + reddit_doors_list), epochs=10)
	print("Door reddit: " + str(model_reddit.wv.most_similar('door', topn=10)))
	print("Wheel reddit: " + str(model_reddit.wv.most_similar('wheel', topn=10)))
	model_wiki = Word2Vec.load('models/base.model')
	model_wiki.train(wiki_wheels_list + wiki_doors_list, total_examples=len(wiki_wheels_list + wiki_doors_list), epochs=10)
	print("Door wiki: " + str(model_wiki.wv.most_similar('door', topn=10)))
	print("Wheel wiki: " + str(model_wiki.wv.most_similar('wheel', topn=10)))