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

We chose logistic regersion because it is one of the fastest models. Speed of the model was the highest priority It is also one of the most accurate. models.  
