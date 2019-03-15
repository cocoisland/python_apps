"""Extract Review and clean into words."""
from decouple import config
from flask import Flask, render_template, request
from .models import DB, ReviewRating
import basilica
BASILICA = basilica.Connection(config('BASILICA_KEY'))

import json
import numpy as np

#import nltk
#nltk.download('stopwords')

import string
from nltk.corpus import stopwords
def text_clean(message):
    nopunc = [i for i in message if i not in string.punctuation]
    nn = "".join(nopunc)
    nn = nn.lower().split()
    nostop = [words for words in nn if words not in stopwords.words('english')]
    nodigit = list(filter(str.isalpha, nostop))
    #nodigit = [''.join(x for x in i if not x.isdigit()) for i in nostop] 
    #nodigit = list(filter(None, nodigit))
    return(nodigit)


def load_local_json():
  DB.drop_all()
  DB.create_all()
  path="./sentiment/data/review.json"
  with open(path, 'r') as f:
    try:
      for line in f:
        data = json.loads(line)
        cleaned_text = text_clean(data['text'])   
        #import pdb; pdb.set_trace()
        #unique_cleaned = set(cleaned_text)
        unique_cleaned = np.unique(cleaned_text).tolist()
        embedding = BASILICA.embed_sentence(data['text'], model='product-reviews')
        stars=data['stars']
        db_review = ReviewRating(stars=data['stars'], review_text=str(unique_cleaned),embedding=embedding)
        DB.session.add(db_review)
        DB.session.commit()

    except Exception as e:
      print('Error processing input review json')
      raise e
    else:
      DB.session.commit()
