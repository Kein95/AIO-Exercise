# -*- coding: utf-8 -*-
"""M2-W4.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ZDguuy1kb8VQXimWlaYsyjQWrXV8xFvU

1. BASIC PROBABILITY
"""

# Question 1
import numpy as np

def compute_mean(X):
  return np.mean(X)

X = [2, 0, 2, 2, 7, 4, -2, 5, -1, -1]

print("Mean : ", compute_mean(X))

# Question 2
import numpy as np

def compute_median(X):
    size = len(X)
    X = np.sort(X)

    if size % 2 == 0:
        median = (X[size // 2 - 1] + X[size // 2]) / 2
    else:
        median = X[size // 2]

    return median

X = [1, 5, 4, 4, 9, 13]

print("Median:", compute_median(X))

# Question 3
import numpy as np

def compute_mean(X):
    return np.mean(X)

def compute_std(X):
    mean = compute_mean(X)
    variance = np.mean((X - mean) ** 2)
    return np.sqrt(variance)

X = np.array([171, 176, 155, 167, 169, 182])
print("Standard Deviation:", np.round(compute_std(X), 2))

# Question 4

def compute_correlation_cofficient(X, Y):
  N = len(X)
  numerator = N * X.dot(Y) - np.sum(X)*np.sum(Y)
  denominator = np.sqrt(N*np.sum(np.square(X))-np.sum(X)**2) \
    * np.sqrt(N*np.sum(np.square(Y))-np.sum(Y)**2)

  return np.round(numerator / denominator,2)

X = np.asarray([-2, -5, -11, 6, 4, 15, 9])
Y = np.asarray([4, 25, 121, 36, 16, 225, 81])
print("Correlation: ", compute_correlation_cofficient(X,Y))

"""2. TABULAR DATA ANALYSIS"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

!gdown 1iA0WmVfW88HyJvTBSQDI5vesf-pgKabq

data = pd.read_csv("./advertising.csv")
data

data.head(5), data.tail(5)

data.info()

# Question 5
def correlation(x, y):
    x_mean = np.mean(x)
    y_mean = np.mean(y)

    numerator = np.sum((x - x_mean) * (y - y_mean))
    denominator = np.sqrt(np.sum((x - x_mean)**2) * np.sum((y - y_mean)**2))

    if denominator == 0:
        return 0  # Handle cases where the denominator is zero

    return numerator / denominator

# Example usage:
x = data['TV']
y = data['Radio']
corr_xy = correlation(x, y)
print(f"Correlation between TV and Sales: {round(corr_xy, 2)}")

# Question 6
features = ['TV', 'Radio', 'Newspaper']

for feature_1 in features:
  for feature_2 in features:
      correlation_value = correlation(data[feature_1], data[feature_2])
      print(f"{feature_1} and {feature_2}: {round(correlation_value, 2)}")

# Question 7
x = data['Radio']
y = data['Newspaper']

result = np.corrcoef(x, y)
print(result)

# Question 8
data_corr_coef = data.corr()
data_corr_coef

# Question 9
plt.figure(figsize=(10,8))
sns.heatmap(data_corr_coef,annot=True, fmt=".2f", linewidth=.5)
plt.show()

"""3. TEXT RETRIEVAL"""

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

!gdown 1jh2p2DlaWsDo_vEWIcTrNh3mUuXd-cw6

# Load dataset
vi_data_df = pd.read_csv("/content/vi_text_retrieval.csv")

# Lowercase the text
context = vi_data_df['text']
context = [doc.lower() for doc in context]

# Question 10
# Initialize TfidfVectorizer
tfidf_vectorizer = TfidfVectorizer()

# Fit and transform the context
context_embedded = tfidf_vectorizer.fit_transform(context)

context_embedded.toarray()[7][0]

# Question 11
def tfidf_search(question, tfidf_vectorizer, top_d=5):
    # Lowercasing before encoding
    query_embedded = tfidf_vectorizer.transform([question.lower()])
    cosine_scores = cosine_similarity(context_embedded, query_embedded).reshape((-1,))

    # Get top k cosine scores and index its
    results = []
    for idx in cosine_scores.argsort()[-top_d:][::-1]:
        doc_score = {
            'id': idx,
            'cosine_score': cosine_scores[idx]
        }
        results.append(doc_score)
    return results

question = vi_data_df.iloc[0]['question']
results = tfidf_search(question, tfidf_vectorizer, top_d=5)
results [0][ 'cosine_score']

# Question 12
def corr_search(question, tfidf_vectorizer, top_d=5):
    query_embedded = tfidf_vectorizer.transform([question.lower()])
    corr_scores = np.corrcoef(
        query_embedded.toarray()[0],
        context_embedded.toarray()
    )
    corr_scores = corr_scores[0][1:]
    results = []
    for idx in corr_scores.argsort()[-top_d:][::-1]:
        doc = {
            'id': idx,
            'corr_score':corr_scores[idx]
        }
        results.append(doc)
    return results

question = vi_data_df.iloc[0]['question']
results = corr_search(question, tfidf_vectorizer, top_d=5)
results [1]['corr_score']