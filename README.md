# CS-547-final: Information Retrevial

* download_data.ipynb
  * Download twitter/Reddit/Wiki data
* search.py
  * Download and train word2vec
* loader.py
  * Load data downloaded from download_data.ipynb
* test.py
  * Train word2vec on text8

## Project Goal
Build a system that can compare two search terms through specialized queries on Social Media and Wikipedia and complete some analysis on those query results

# Project takeaways

## Wheels or doors?
Wheels seems to win!

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
