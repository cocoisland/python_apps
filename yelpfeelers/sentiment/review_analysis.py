"""Prediction of Users based on Tweet embeddings."""
import pandas as pd
from .models import ReviewRating
from .load_text import text_clean
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB


def fetchRating():
  i=0
  df = pd.DataFrame(columns=['id','stars','review_text','embedding'])
  allReview = ReviewRating.query.all()
  for r in allReview:
    df.loc[i] = (r.id, r.stars, r.review_text, r.embedding)
    i += 1
  return df

  
def prep_basilica_X(df):
  x = df['embedding']
  return x

def prep_X(df, ptext):
  x = df['review_text']
  series_ptext = pd.Series(ptext)
  x = x.append(series_ptext, ignore_index=True)
  cv_transformer = CountVectorizer(analyzer = text_clean)
  x= cv_transformer.fit_transform(x)
  return x[:-1], x[-1:]


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

def train_model(x, y):
  nb = MultinomialNB()
  nb.fit(x,y)
  return nb

# predict by countvectorizer
def predict_text(predict_str):
  df = fetchRating()
  x, x_pred = prep_X(df,predict_str)
  y = prep_Y(df)
  model = train_model(x,y)
  prediction = model.predict(x_pred)
  return prediction

from sklearn.linear_model import LogisticRegression

def predict_basilica(predict_str):
  df = fetchRating()
  x = prep_basilica_X(df)
  y = prep_Y(df)
  model = LogisticRegression().fit(x,y)

  x_pred = BASILICA.embed_sentence(predict_str, model='product-reviews')
  prediction = model.predict(x_pred.reshape(1,-1))
  return prediction
