# CS-547-final: Information Retrevial
To see the website, go to: https://wheeleddoors.github.io/index/
(for best results, turn off ad-blocker. We won’t spam you, we promise)

## Project Goal
A project that originated around a meme of whether there are more wheels or doors in the world, it branched into having a general goal of being able to compare two search terms. In the end, our project goal was to: build a system that can compare two search terms through specialized queries on Social Media and Wikipedia and complete some analysis on those query results.
# Methodology

## Word2Vec

We decided to use word2vec to find words similar to the search word. There was one base model that was trained on text8. Each time that a user does a query on a word, the base model is fine-tuned on each of the 3 data sources. The data sources were Twitter, Reddit, and Wikipedia. 

## Sentement Analysis

One of our goals was to create a sentiment analysis algorithm to understand more about the general feelings towards the inputted key search terms. One issue to this goal is that each query will produce a brand new, unlabeled dataset, so to work around this, we trained methods on a general twitter dataset to get a general baseline moddel. While this won't great a perfect accuracy, the hope was to create a model that can give a general  idea of the sentimenet around each word. 

| Model Name | Preprocessing | 50k Avg Accuracy | 100k Avg Accuracy |
| -----------|---------------|------------------|-------------------|
| Naive Bayes| BOW | 0.782 | 0.753 |
| Logistic Regr. | BOW | 0.775 | 0.771 |
| Random Forest | BOW | 0.707 | 0.742 |
| Support Vector | BOW | 0.726 | 0.767 | 
| Naive Bayes | TFIDF | 0.774 | 0.702 | 
| Logistic Regr. | TFIDF | 0.781 | 0.773 | 
| Random Forest | TFIDF | 0.717 | 0.758 | 
| Support Vector | TFIDF | 0.736 | 0.774 | 
| Naive Bayes | Word2Vec | 0.624 | 0.624 | 
| Logistic Regr. | Word2Vec | 0.693 | 0.702 | 
| Random Forest | Word2Vec | 0.662 | 0.664 | 
| Support Vector | Word2Vec | 0.710 | 0.725 | 
| Bert | None | 0.501 | 0.662 | 
| Average Word | None | 0.651 | 0.646 | 

We choose Naive Bayes with Bag of Words preprocessing as it had the most successful testing error unde the 50,000 training point build and was in the faster group of models. 

## Topic Modeling

The last goal of our method was the complete topic modeling for each of the query results. This was simple to achieve using a LDA method as it was an unsupervised model so required no pre-training. This method returns 3 total topics with the top 10 words per topic. 

## Web Interface and AWS API

To implement our code into one final design, we developed both a front end web interface and a backend AWS lambda function API that lives on a docker station. The front end shows off  the model results in a fun and interactive way, including smiley faces that change with varying levels of sentiment scores. While the backend API was able to run in the end, due to AWS API call length limitations, it was never fully connected to the front end. We have uploaded data into our front end with the original search terms of “door” and “wheel”, seen here: https://wheeleddoors.github.io/index/ 


# Project Takeaways

WHile this project was interesting and presented indivdual learning challenges to each of us, we don't recommend attempting such a large and expansive project on student resources. With more resource, i.e. money and computing capabilities, we hope to see this project improve including improving speed, allowing for users to determine how many topics and with corpouses, and general mprovements to the web intereface. 

## So, which is actually more prevelant: wheels or doors?
While we don't know the true answer, we can at least say that in the publics eyes based off of sentiment analysis: Wheels seems to win!

