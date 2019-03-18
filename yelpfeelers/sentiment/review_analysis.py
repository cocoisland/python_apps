"""Prediction of Users based on Tweet embeddings."""
import pandas as pd
from .models import ReviewRating
from .load_text import text_clean, BASILICA
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import numpy as np
import pickle


def fetchRating():
  i=0
  df = pd.DataFrame(columns=['id','stars','review_text','embedding'])
  allReview = ReviewRating.query.all()
  for r in allReview:
    df.loc[i] = (r.id, r.stars, r.review_text, r.embedding)
    i += 1
  return df

def prep_Y(df):
  Cust = []
  for i in df['stars']:
    if (i == 1):
        Cust.append('BAD')
    elif (i == 3) | (i == 2):
        Cust.append('NEUTRAL')
    else:
        Cust.append('GOOD')

  df['threeStars'] = Cust
  y = df['threeStars']
  return y
  

def countVectorizer_encoding(ptext):
  df = fetchRating()
  x = df['review_text']
  series_ptext = pd.Series(ptext)
  x = x.append(series_ptext, ignore_index=True)
  cv_transformer = CountVectorizer(analyzer = text_clean)
  x= cv_transformer.fit_transform(x)

  y = prep_Y(df)
  return x[:-1],y, x[-1:]


def train_multinomialNB(x, y):
  nb = MultinomialNB()
  nb.fit(x,y)
  return nb

from sklearn.linear_model import LogisticRegression

def train_basilica():
  try:
    model = pickle.load(open("./sentiment/model.pickle", "rb"))
  except (OSError, IOError) as e:
    df = fetchRating()
    x = df['embedding']
    x = np.stack(x, axis=0)

    y = prep_Y(df)
    model = LogisticRegression(solver='lbfgs',multi_class='auto').fit(x,y)
    pickle.dump(model, open("./sentiment/model.pickle", "wb"))

  return model
