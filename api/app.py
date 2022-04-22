import gensim.downloader
import json

def handler(event, context):
	print("Received event: " + str(event))
	poc_lambda()
	return {
		'statusCode': 200,
		'body': json.dumps('Hello from Lambda!')
	}


def poc_lambda():
	glove_vectors = gensim.downloader.load('glove-twitter-25')
	print("Word2Vec model glove-twitter-200 loaded")
	print("Door vector: " + glove_vectors['door'])
	print("Wheel vector: " + glove_vectors['wheel'])
	print(glove_vectors.most_similar('door'))
	print(glove_vectors.most_similar('wheel'))
