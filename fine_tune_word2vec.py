from turtle import goto
import gensim.downloader

if __name__ == "__main__":
	# Fine-tune the word2vec model form txt file
	glove_vectors = gensim.downloader.load('glove-wiki-gigaword-300')
	print("Word2Vec model wiki-gigaword-300 loaded")
	print("Door vector: " + glove_vectors['door'])
	print("Wheel vector: " + glove_vectors['wheel'])
	print(glove_vectors.most_similar('door'))
	print(glove_vectors.most_similar('wheel'))
	glove_vectors = gensim.downloader.load('glove-twitter-200')
	print("Word2Vec model glove-twitter-200 loaded")
	print("Door vector: " + glove_vectors['door'])
	print("Wheel vector: " + glove_vectors['wheel'])
	print(glove_vectors.most_similar('door'))
	print(glove_vectors.most_similar('wheel'))
