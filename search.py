from gensim.models import Word2Vec
import requests
import json
import time
import praw
from bs4 import BeautifulSoup
import glob

def get_tweets(search, num_tweets = 5):
    
	with open('key.json') as f:
		key = json.load(f)
		bearer_token = key['BEARER_TOKEN']
 
	# Create the url
	url = 'https://api.twitter.com/1.1/search/tweets.json?result_type=popular&q='+ search + '&max_results=' + str(num_tweets)
	# Create request headers
	headers = {
		'authorization': 'Bearer ' + bearer_token,
		'user-agent': 'v2FilteredStreamPython',
	}
	# Make the request
	response = requests.get(url, headers=headers)
	return response.json()

def get_wikipedia_data(search, num_posts = 5):
	# Create the url for the search also get the posts text
	url = 'https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch=' + search + '&format=json&srlimit=' + str(num_posts)
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
	
	for page in wiki_search['query']['search']:
		url = 'https://en.wikipedia.org/wiki/' + page['title']
		response = requests.get(url)
		soup = BeautifulSoup(response.text, 'html.parser')
		file_name = 'data/wiki/tmp/' + page['title'] + '.txt'
		# Make file name compatible with windows
		file_name = file_name.replace(' ', '_').replace(':', '_').replace('\\', '_').replace('"', '_').replace('?', '_').replace('*', '_').replace('|', '_').replace('<', '_').replace('>', '_')
		with open(file_name, 'w') as f:
			f.write(soup.get_text())
		time.sleep(0.1)
	
		files_wiki = glob.glob('data/wiki/tmp/*.txt')
		text_wiki = []
		for f in files_wiki:
			with open(f, 'r') as f:
				text = f.read()
				# remove duplicate \n
				for _ in range(100):
					text = text.replace('\n\n', '\n')
				text_wiki.append(text)
 
	# Split into sentences
	tweets_text = split_into_sentences(tweets_text)
	reddit_text = split_into_sentences(reddit_text)
	text_wiki = split_into_sentences(text_wiki)

	model_twitter = Word2Vec.load("models/base.model")
	model_reddit = Word2Vec.load("models/base.model")
	model_wiki = Word2Vec.load("models/base.model")
	
	# Train the model
	model_twitter.train(tweets_text, total_examples=len(tweets_text), epochs=10)
	model_reddit.train(reddit_text, total_examples=len(reddit_text), epochs=10)
	model_wiki.train(text_wiki, total_examples=len(text_wiki), epochs=10)
	
	twitter_top = model_reddit.wv.most_similar(word, topn=10)
	reddit_top = model_reddit.wv.most_similar(word, topn=10)
	wiki_top = model_wiki.wv.most_similar(word, topn=10)
	print(word + " twitter: " + str(twitter_top))
	print(word + " reddit: " + str(reddit_top))
	print(word + " wiki: " + str(wiki_top))
	
	return twitter_top, reddit_top, wiki_top


if __name__=="__main__":
	search("computer")
